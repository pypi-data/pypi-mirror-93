#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetClientBase, DatasetClient, FusionDatasetClient,
SegmentClientBase, SegmentClient, FusionSegmentClient
"""

import os
import threading
import time
import uuid
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, TypeVar, Union

import filetype
from requests_toolbelt import MultipartEncoder

from ..dataset import Data, Frame, FusionSegment, Segment
from ..label import Catalog
from ..sensor import Camera, FisheyeCamera, Sensor
from ..utility import TBRN, NameSortedDict, TBRNType
from .exceptions import GASException, GASPathError, GASSegmentError
from .requests import Client, default_config, multithread_upload, post

_T = TypeVar("_T", bound=Sensor)

_SERVER_VERSION_MATCH: Dict[str, str] = {
    "AmazonS3": "x-amz-version-id",
    "AliyunOSS": "x-oss-version-id",
}


class SegmentClientBase:
    """This class defines the concept of a segment client and some opertions on it.

    :param name: Segment name, unique for a dataset
    :param dataset_id: Dataset Id
    :param dataset_name: Dataset name
    :param client: The client used for sending request to TensorBay
    :param commit_id: Dataset commit ID
    """

    _PERMISSION_CATEGORY: str
    _EXPIRED_IN_SECOND = 240

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        self._name = name
        self._dataset_id = dataset_id
        self._dataset_name = dataset_name
        self._client = client
        self._commit_id = commit_id
        self._permission: Dict[str, Any] = {"expireAt": 0}
        self._permission_lock = threading.Lock()

    @property
    def name(self) -> str:
        """Get the name of this segment client.

        :return: The name of the segment
        """
        return self._name

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    @property
    def commit_id(self) -> Optional[str]:
        """Get the dataset commit ID.

        :return: The dataset commit ID
        """
        return self._commit_id

    def _get_url(self, tbrn: TBRN) -> str:
        """Get url of specific remote_path

        :param tbrn: TensorBay Resource Name
        :return: The url of the input remote_path and sensor_name
        """
        post_data = {
            "segmentName": self._name,
            "remotePath": tbrn.remote_path,
        }
        if tbrn.type == TBRNType.FUSION_FILE:
            post_data["sensorName"] = tbrn.sensor_name
        response = self._client.open_api_get("data/urls", post_data, dataset_id=self.dataset_id)
        return response.json()["url"]  # type: ignore[no-any-return]

    def _list_labels(self) -> Generator[Dict[str, Any], None, None]:
        """List labels in a segment client.

        :return: A generator of labels
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        while True:
            params["offset"] = offset
            response = self._client.open_api_get(
                "labels", params, dataset_id=self.dataset_id
            ).json()
            yield from response["labels"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def _get_upload_permission(self) -> Dict[str, Any]:
        with self._permission_lock:
            if int(time.time()) >= self._permission["expireAt"]:
                post_data = {
                    "expired": self._EXPIRED_IN_SECOND,
                    "segmentName": self._name,
                }
                self._permission = self._client.open_api_get(
                    "policies", post_data, dataset_id=self.dataset_id
                ).json()

                if default_config.is_intern:
                    urlsplit = self._permission["extra"]["host"].rsplit(".", 2)
                    urlsplit[0] += "-internal"
                    self._permission["extra"]["host"] = ".".join(urlsplit)

            return deepcopy(self._permission)

    def _clear_upload_permission(self) -> None:
        with self._permission_lock:
            self._permission = {"expireAt": 0}

    @staticmethod
    def _post_multipart_formdata(
        url: str,
        local_path: str,
        remote_path: str,
        data: Dict[str, Any],
    ) -> Tuple[str, str]:
        with open(local_path, "rb") as fp:
            file_type = filetype.guess_mime(local_path)
            if "x-amz-date" in data:
                data["Content-Type"] = file_type
            data["file"] = (remote_path, fp, file_type)
            multipart = MultipartEncoder(data)
            headers = post(url, data=multipart, content_type=multipart.content_type).headers
            version = _SERVER_VERSION_MATCH[headers["Server"]]
            return headers[version], headers["ETag"].strip('"')

    def _synchronize_upload_info(
        self, key: str, version_id: str, etag: str, frame_info: Optional[Dict[str, Any]] = None
    ) -> None:
        post_data = {
            "key": key,
            "versionId": version_id,
            "etag": etag,
        }
        if frame_info:
            post_data.update(frame_info)

        self._client.open_api_put("callback", post_data, dataset_id=self.dataset_id)

    def _upload_label(self, data: Data) -> None:
        post_data: Dict[str, Any] = {
            "segmentName": self.name,
            "remotePath": data.remote_path,
            "labelValues": data._dump_labels(),
        }
        self._client.open_api_post("labels", post_data, dataset_id=self.dataset_id)


class SegmentClient(SegmentClientBase):
    """ContentSegmentClient has only one sensor, supporting upload_data method."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        super().__init__(name, dataset_id, dataset_name, client, commit_id)

    def upload_data(self, local_path: str, remote_path: str = "") -> None:
        """Upload data with local path to the segment.

        :param local_path: The local path of the data to upload
        :param remote_path: The path to save the data in segment client
        :raises
            GASPathError: when remote_path does not follow linux style
            GASFrameError: when uploading frame has neither timestamp nor frame_index
        """

        if not remote_path:
            remote_path = os.path.basename(local_path)

        if "\\" in remote_path:
            raise GASPathError(remote_path)

        permission = self._get_upload_permission()
        post_data = permission["result"]
        post_data["key"] = permission["extra"]["objectPrefix"] + remote_path

        del post_data["x:category"]
        del post_data["x:id"]
        try:
            version_id, etag = self._post_multipart_formdata(
                permission["extra"]["host"],
                local_path,
                remote_path,
                post_data,
            )

            self._synchronize_upload_info(post_data["key"], version_id, etag)

        except GASException:
            self._clear_upload_permission()
            raise

    def upload_label(self, data: Data) -> None:
        """Upload label with Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self._upload_label(data)

    def upload_data_object(self, data: Data) -> None:
        """Upload data with Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self.upload_data(data.local_path, data.remote_path)
        self._upload_label(data)

    def delete_data(self, remote_paths: Union[str, List[str]]) -> None:
        """Delete data with remote paths.

        :param remote_paths: A single path or a list of paths which need to deleted,
        eg: test/os1.png or [test/os1.png]
        """
        self._content_segment_client.delete_data(remote_paths)

    def _list_data(self) -> Generator[Dict[str, Any], None, None]:
        """List data in a segment client.

        :return: A generator of data
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get("data", params, dataset_id=self.dataset_id).json()
            yield from response["data"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_data(self) -> Generator[str, None, None]:
        """List all data path in a segment client.

        :return: A generator of data path
        """
        return (item["remotePath"] for item in self._list_data())

    def list_data_objects(self) -> Generator[Data, None, None]:
        """List all `Data` object in a dataset segment.

        :return: A generator of `Data` object
        """
        for labels in self._list_labels():
            remote_path = labels["remotePath"]
            tbrn = TBRN(self._dataset_name, self._name, remote_path=remote_path)
            data = Data(tbrn, url_getter=self._get_url)
            data.load_labels(labels["label"])
            yield data


class FusionSegmentClient(SegmentClientBase):
    """FusionSegmentClient has multiple sensors,
    supporting upload_sensor and upload_frame method.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_id: str,
        dataset_name: str,
        client: Client,
        commit_id: Optional[str] = None,
    ) -> None:
        super().__init__(name, dataset_id, dataset_name, client, commit_id)

    def upload_sensor_object(self, sensor: _T) -> None:
        """Upload sensor to the segment client.

        :param sensor: The sensor to upload
        """
        post_data = {
            "name": sensor.name,
            "type": sensor.enum.value,
            "extrinsicParams": sensor.extrinsics.dumps() if sensor.extrinsics else {},
        }

        if isinstance(sensor, (Camera, FisheyeCamera)):
            if sensor.intrinsics:
                intrinsics = sensor.intrinsics.dumps()
                intrinsics["distortionCoefficient"] = intrinsics.pop("distortionCoefficients", {})
                post_data["intrinsicParams"] = intrinsics
            else:
                post_data["intrinsicParams"] = {}

        if sensor.description:
            post_data["desc"] = sensor.description

        post_data["segmentName"] = self._name
        self._client.open_api_post("sensors", post_data, dataset_id=self.dataset_id)

    def upload_frame_object(self, frame: Frame, frame_index: Optional[int] = None) -> None:
        """Upload frame to the segment client.

        :param frame: The frame to upload
        :param frame_index: The frame index, used for TensorBay to sort the frame
        :raises
            GASPathError: when remote_path does not follow linux style
        """

        frame_id = str(uuid.uuid4())

        for sensor_name, data in frame.items():
            remote_path = data.remote_path

            if "\\" in remote_path:
                raise GASPathError(remote_path)

            if frame_index is None and not hasattr(data, "timestamp"):
                raise TypeError(
                    "Either 'frame_index' or 'timestamp' is necessary for sorting frames"
                )

            permission = self._get_upload_permission()
            post_data = permission["result"]

            path = str(PurePosixPath(sensor_name, remote_path))
            post_data["key"] = permission["extra"]["objectPrefix"] + path

            del post_data["x:category"]
            del post_data["x:id"]

            try:
                version_id, etag = self._post_multipart_formdata(
                    permission["extra"]["host"],
                    data.local_path,
                    remote_path,
                    post_data,
                )

                frame_info: Dict[str, Any] = {
                    "segmentName": self._name,
                    "sensorName": sensor_name,
                    "frameId": frame_id,
                }
                if hasattr(data, "timestamp"):
                    frame_info["timestamp"] = data.timestamp
                if frame_index is not None:
                    frame_info["frameIndex"] = frame_index

                self._synchronize_upload_info(post_data["key"], version_id, etag, frame_info)

            except GASException:
                self._clear_upload_permission()
                raise
            self._upload_label(data)

    def delete_sensors(self, sensor_names: Union[str, List[str]]) -> None:
        """Delete sensors with a single name or a name list.

        :param sensor_names: A single sensor name or a list of sensor names
        """
        self._content_segment_client.delete_sensors(sensor_names)

    def _list_frames(self) -> Generator[Dict[str, Any], None, None]:
        """List all frames in a segment client(Fusion dataset).

        :return: A generator of fusion data
        """
        offset, page_size = 0, 128
        params: Dict[str, Any] = {"segmentName": self._name}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get("data", params, dataset_id=self.dataset_id).json()
            yield from response["data"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_frame_objects(self) -> Generator[Frame, None, None]:
        """List all frames in the segment.

        :return: A list `Frame` object
        """
        for frame_index, labels in enumerate(self._list_labels()):
            frame = Frame()
            for data_info in labels["frame"]:
                loads = data_info["label"]
                sensor_name = data_info["sensorName"]
                remote_path = data_info["remotePath"]
                loads["timestamp"] = data_info["timestamp"]
                tbrn = TBRN(
                    self._dataset_name,
                    self._name,
                    frame_index,
                    sensor_name,
                    remote_path=remote_path,
                )
                loads["fileuri"] = tbrn
                frame[sensor_name] = Data.loads(loads)
            yield frame

    def list_sensors(self) -> List[str]:
        """List all sensor names in a segment client.

        :return: A list of sensor name
        """
        return self._content_segment_client.list_sensors()

    def list_sensor_objects(self) -> NameSortedDict[Sensor]:
        """List all sensors in a segment client.

        :return: A NameSortedDict of `Sensor` object
        """
        return self._content_segment_client.list_sensor_objects()


class DatasetClientBase:
    """This class defines the concept of a dataset and some operations on it.

    :param name: Dataset name
    :param dataset_id: Dataset id
    :param client: The client used for sending request to TensorBay
    :param commit_id: The dataset commit Id
    """

    def __init__(
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        self._name = name
        self._dataset_id = dataset_id
        self._client = client
        self._commit_id = commit_id

    def set_description(self, description: str) -> None:
        """Set description of the dataset.

        :param description: description of the dataset
        """
        post_data = {
            "datasetId": self._dataset_id,
            "desc": description,
        }
        self._client.dataset_post("updateDataset", post_data)

    @property
    def commit_id(self) -> Optional[str]:
        """Get the dataset commit Id

        :return: The dataset commit Id
        """
        return self._commit_id

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    def _commit(self, message: str, tag: Optional[str] = None) -> str:
        post_data = {
            "message": message,
        }
        if tag:
            post_data["tag"] = tag

        response = self._client.open_api_post("", post_data, dataset_id=self.dataset_id)
        return response.json()["commitId"]  # type: ignore[no-any-return]

    def _create_segment(self, name: str) -> None:
        post_data = {"name": name}
        self._client.open_api_post("segments", post_data, dataset_id=self.dataset_id)

    def _list_segments(self) -> Generator[str, None, None]:
        offset, page_size = 0, 128
        params: Dict[str, Any] = {}
        if self._commit_id:
            params["commit"] = self._commit_id
        while True:
            params["offset"] = offset
            response = self._client.open_api_get(
                "segments", params, dataset_id=self.dataset_id
            ).json()
            yield from response["segments"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_segments(self) -> Generator[str, None, None]:
        """List all segment names in a dataset.

        :return: A generator of segment names
        """
        return self._list_segments()

    def delete_segments(
        self,
        segment_names: Union[str, List[str]],
        force_delete: bool = False,
    ) -> None:
        """Delete segments according to the name list.

        :param name: A single segment Name or a list of the segment names, if empty, the default
        segment will be deleted, if you want to delete all segment, "_all" should be submitted.
        :param force_delete: By default, only segment with no sensor can be deleted.
        If force_delete is true, then sensor and its objects will also be deleted
        """
        self._contentset_client.delete_segments(segment_names, force_delete)

    def upload_catalog(self, catalog: Catalog) -> None:
        """Upload a Catalog to the dataset,

        :param catalog: The `Catalog` object to upload
        """
        catalog_data = catalog.dumps()
        if not catalog_data:
            raise TypeError("Empty catalog")

        self._client.open_api_put("labels/catalogs", catalog_data, dataset_id=self.dataset_id)


class DatasetClient(DatasetClientBase):
    """dataset has only one sensor, supporting create segment."""

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        super().__init__(name, dataset_id, client, commit_id)

    def get_or_create_segment(self, name: str = "_default") -> SegmentClient:
        """Create a segment set according to its name.

        :param name: Segment name, can not be "_default"
        :return: Created segment with given name, if not given name, Created default segment
        """
        if name not in self._list_segments():
            self._create_segment(name)
        return SegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment(self, name: str = "_default") -> SegmentClient:
        """Get a segment according to its name.

        :param name: The name of the desired segment
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment
        """
        if name not in self._list_segments():
            raise GASSegmentError(name)

        return SegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment_object(self, name: str = "_default") -> Segment:
        """Get a segment object according to its name.

        :param name: The name of the desired segment object
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment object
        """
        segment_client = self.get_segment(name)
        segment = Segment(name)
        for data in segment_client.list_data_objects():
            segment.append(data)

        return segment

    def upload_segment_object(
        self,
        segment: Segment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> SegmentClient:
        """Upload a `Segment` to the contentset,
        This function will upload all info contains in the input `Segment` object,
        which includes:
        - Create a segment using the name of input `Segment`
        - Upload all `Data` in the Segment to the contentset

        :param segment: The `Segment` object contains the information needs to be upload
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `Segment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        segment_filter: Iterable[Data]
        if skip_uploaded_files:
            done_set = set(segment_client.list_data())
            segment_filter = filter(lambda data: data.remote_path not in done_set, segment)
        else:
            segment_filter = segment

        multithread_upload(segment_client.upload_data_object, segment_filter, jobs=jobs)
        return segment_client

    def commit(self, message: str, tag: Optional[str] = None) -> "DatasetClient":
        """
        Commit dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed dataset client
        """
        commit_id = self._commit(message, tag)
        return DatasetClient(self._name, self.dataset_id, self._client, commit_id)


class FusionDatasetClient(DatasetClientBase):
    """Client for fusion dataset which has multiple sensors,
    supporting create fusion segment.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, commit_id: Optional[str] = None
    ) -> None:
        super().__init__(name, dataset_id, client, commit_id)

    def get_or_create_segment(self, name: str = "_default") -> FusionSegmentClient:
        """Create a fusion segment set according to the given name.

        :param name: Segment name, can not be "_default"
        :return: Created fusion segment with given name, if not given name, Created default segment
        """
        if name not in self._list_segments():
            self._create_segment(name)
        return FusionSegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def get_segment(self, name: str = "_default") -> FusionSegmentClient:
        """Get a fusion segment according to its name.

        :param name: The name of the desired fusion segment
        :raises GASSegmentError: When the required fusion segment does not exist
        :return: The desired fusion segment
        """
        if name not in self._list_segments():
            raise GASSegmentError(name)
        return FusionSegmentClient(name, self._dataset_id, self._name, self._client, self.commit_id)

    def upload_segment_object(
        self,
        segment: FusionSegment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionSegmentClient:
        """Upload a `FusionSegment` to the contentset,
        This function will upload all info contains in the input `FusionSegment` object,
        which includes:
        - Create a segment using the name of input `FusionSegment`
        - Upload all `Sensor` in the segment to the contentset
        - Upload all `Frame` in the segment to the contentset

        :param segment: The `Segment` object needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `FusionSegment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        sensors = segment.get_sensors()
        for sensor in sensors.values():
            segment_client.upload_sensor_object(sensor)

        segment_filter: Iterable[Tuple[int, Frame]]
        if skip_uploaded_files:
            # TODO: skip_uploaded_files
            segment_filter = enumerate(segment)
        else:
            segment_filter = enumerate(segment)

        multithread_upload(
            lambda args: segment_client.upload_frame_object(args[1], args[0]),
            segment_filter,
            jobs=jobs,
        )

        return segment_client

    def commit(self, message: str, tag: Optional[str] = None) -> "FusionDatasetClient":
        """
        Commit fusion dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed fusion dataset client
        """
        commit_id = self._commit(message, tag)
        return FusionDatasetClient(self._name, self.dataset_id, self._client, commit_id)
