#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class GAS."""

from typing import Any, Dict, Generator, Iterable, Optional, Tuple, Type, Union, overload
from urllib.parse import urljoin

from typing_extensions import Literal

from ..dataset import Dataset, DataType, FusionDataset, _DataType
from .dataset import DatasetClient, FusionDatasetClient
from .exceptions import GASDatasetError, GASDatasetTypeError, GASDataTypeError
from .requests import Client, get

DatasetClientType = Union[DatasetClient, FusionDatasetClient]
DATATYPE_MAP = {
    DataType.IMAGE: 0,
    DataType.POINT_CLOUD: 1,
    DataType.AUDIO: 2,
    DataType.TEXT: 3,
    DataType.OTHERS: 255,
}


# pylint: disable=too-many-public-methods
class GAS:
    """This is a class defining the concept of TensorBay.
    It mainly defines some operations on datasets.

    :param access_key: user's access key
    :param url: the url of the gas website
    """

    _VERSIONS = {1: "COMMUNITY", 2: "ENTERPRISE"}

    def __init__(self, access_key: str, url: str = "") -> None:
        self._client = Client(access_key, url)

    def get_user_info(self) -> Dict[str, str]:
        """Get the user info corresponding to the AccessKey

        :return: A directory which contains the username and clientTag
        """
        post_data = {"token": self._client.access_key}
        url = urljoin(self._client.gateway_url, "user/api/v3/token/get-user-profile")
        response = get(url, params=post_data).json()["data"]
        return {
            "username": response["userName"],
            "version": GAS._VERSIONS[response["clientTag"]],
        }

    @overload
    def _create_dataset(
        self,
        name: str,
        is_continuous: bool,
        is_fusion: Literal[False],
        data_type: Optional[_DataType] = None,
    ) -> DatasetClient:
        ...

    @overload
    def _create_dataset(
        self,
        name: str,
        is_continuous: bool,
        is_fusion: Literal[True],
        data_type: Union[Iterable[_DataType], _DataType, None] = None,
    ) -> FusionDatasetClient:
        ...

    def _create_dataset(
        self,
        name: str,
        is_continuous: bool,
        is_fusion: bool,
        data_type: Union[Iterable[_DataType], _DataType, None] = None,
    ) -> DatasetClientType:
        post_data = {
            "name": name,
            "type": int(is_fusion),  # normal dataset: 0, fusion dataset: 1
            "isContinuous": is_continuous,
        }
        if data_type:
            if isinstance(data_type, Iterable):  # pylint: disable=W1116
                if not is_fusion:
                    raise GASDataTypeError()

                post_data["dataType"] = [data_type.value for data_type in data_type]
            else:
                post_data["dataType"] = [data_type.value]

        response = self._client.open_api_post("", post_data)
        ReturnType: Type[DatasetClientType] = FusionDatasetClient if is_fusion else DatasetClient
        return ReturnType(name, response.json()["id"], self._client)

    def create_dataset(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Optional[_DataType] = None,
    ) -> DatasetClient:
        """Create a dataset with the input name,
        and return the client of the created dataset

        :param name: Name of the dataset, unique for a user
        :param is_continuous: Whether the data in dataset are continuous,
            `True` for continuous data, `False` for Discontinuous data
        :param data_type: Type of the data
        :return: The client of the created dataset
        """
        return self._create_dataset(name, is_continuous, False, data_type)

    def create_fusion_dataset(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Union[Iterable[_DataType], _DataType, None] = None,
    ) -> FusionDatasetClient:
        """Create a fusion contentset with the input name,
        and return the client of the created fusion contentset

        :param name: Name of the fusion contentset, unique for a user
        :param is_continuous: Whether the data in contentset are continuous,
            `True` for continuous data, `False` for Discontinuous data
        :param data_type: Type of the data
        :return: The client of the created fusion contentset
        """
        return self._create_dataset(name, is_continuous, True, data_type)

    def _get_dataset(self, name: str, commit_id: Optional[str] = None) -> DatasetClientType:
        """Get the client of the dataset with the input name no matter the type of the dataset

        :param name: The name of the requested dataset
        :param commit_id: The dataset commit Id
        :raises GASDatasetError: When the requested dataset does not exist
        :return: The client of the request dataset
        """
        dataset_id, is_fusion = self._get_dataset_id_and_type(name)
        ReturnType: Type[DatasetClientType] = FusionDatasetClient if is_fusion else DatasetClient
        return ReturnType(name, dataset_id, self._client, commit_id)

    def get_dataset(self, name: str, commit_id: Optional[str] = None) -> DatasetClient:
        """Get the client of the dataset with the input name

        :param name: The name of the requested dataset
        :param commit_id: The dataset commit Id
        :raises GASDatasetError: When the requested dataset does not exist
        :raises GASDatasetTypeError: When requested dataset is a fusion dataset
        :return: The client of the request dataset
        """
        client = self._get_dataset(name, commit_id)
        if not isinstance(client, DatasetClient):
            raise GASDatasetTypeError(name, True)

        return client

    def get_fusion_dataset(self, name: str, commit_id: Optional[str] = None) -> FusionDatasetClient:
        """Get the client of the fusion dataset with the input name

        :param name: The name of the requested fusion dataset
        :param commit_id: The dataset commit Id
        :raises GASDatasetError: When the requested dataset does not exist
        :raises GASDatasetTypeError: When requested dataset is not a fusion dataset
        :return: The client of the request fusion dataset
        """
        client = self._get_dataset(name, commit_id)
        if not isinstance(client, FusionDatasetClient):
            raise GASDatasetTypeError(name, False)

        return client

    def get_or_create_dataset(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Optional[_DataType] = None,
        commit_id: Optional[str] = None,
    ) -> DatasetClient:
        """Get a dataset if 'name' exists. Create one otherwise.

        :param name: The name of a dataset
        :param is_continuous: Whether the data in dataset are continuous,
            `True` for continuous data, `False` for Discontinuous data
        :param data_type: Type of the data
        :param commit_id: The dataset commit Id
        :raises GASDatasetTypeError: When requested dataset is a fusion dataset
        :return: created dataset
        """
        try:
            return self.get_dataset(name, commit_id)
        except GASDatasetError:
            return self.create_dataset(name, is_continuous, data_type)

    def get_or_create_fusion_dataset(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Union[Iterable[_DataType], _DataType, None] = None,
        commit_id: Optional[str] = None,
    ) -> FusionDatasetClient:
        """Get a dataset if 'name' exists. Create one otherwise.

        :param name: The name of a dataset
        :param is_continuous: Whether the data in dataset are continuous,
            `True` for continuous data, `False` for Discontinuous data
        :param data_type: Type of the data
        :param commit_id: The dataset commit Id
        :raises GASDatasetTypeError: When requested dataset is not a fusion dataset
        :return: created dataset
        """
        try:
            return self.get_fusion_dataset(name, commit_id)
        except GASDatasetError:
            return self.create_fusion_dataset(name, is_continuous, data_type)

    def _list_datasets(
        self,
        name: Optional[str] = None,
        need_team_dataset: bool = False,  # personal: False, all: True
    ) -> Generator[Dict[str, Any], None, None]:

        offset, page_size = 0, 128
        params: Dict[str, Any] = {}
        if name:
            params["name"] = name
        if need_team_dataset:
            params["needTeamDataset"] = need_team_dataset

        while True:
            params["offset"] = offset
            response = self._client.open_api_get("", params).json()
            yield from response["datasets"]
            if response["recordSize"] + offset >= response["totalCount"]:
                break
            offset += page_size

    def list_datasets(self) -> Generator[str, None, None]:
        """List names of all datasets.

        :return: A Generator of names of all datasets
        """
        return (item["name"] for item in self._list_datasets())

    def _get_dataset_id_and_type(self, name: str) -> Tuple[str, bool]:
        """Get the dataset ID and the type of the contentset with the input name

        :param name: The name of the requested contentset
        :raises GASDatasetError: When the requested contentset does not exist
        :return: The tuple of contentset ID and type (`True` for fusion contentset)
        """
        if not name:
            raise GASDatasetError(name)

        try:
            info = next(self._list_datasets(name))
        except StopIteration as error:
            raise GASDatasetError(name) from error

        return (
            info["id"],
            bool(info["type"]),
        )

    def delete_dataset(self, name: str) -> None:
        """Delete a dataset according to its name.

        :param name: The name of the dataset to delete
        :raises GASDatasetError: When the requested contentset does not exist
        """
        dataset_id, _, _, _ = self._get_dataset_id_and_type(name)
        post_data = {"datasetId": dataset_id}
        self._client.dataset_post("deleteDataset", post_data)

    @overload
    def upload_dataset_object(
        self,
        dataset: Dataset,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> DatasetClient:
        ...

    @overload
    def upload_dataset_object(
        self,
        dataset: FusionDataset,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionDatasetClient:
        ...

    @overload
    def upload_dataset_object(
        self,
        dataset: Union[Dataset, FusionDataset],
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> DatasetClientType:
        ...

    def upload_dataset_object(
        self,
        dataset: Union[Dataset, FusionDataset],
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> DatasetClientType:
        """Upload a `Dataset` or `FusionDataset` to TensorBay,
        This function will upload all info contains in the `Dataset` or `FusionDataset` object,
        which includes:
        - Create a dataset using the name and type of input `Dataset` or `FusionDataset`,
        - Upload all `Segment` or `FusionSegment` in the dataset to TensorBay

        :param dataset: The `Dataset` or `FusionDataset` object needs to be uploaded.
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The `ContentsetClient` or `FusionContentsetClient` used for uploading the dataset
        """
        data_type = dataset.data_type
        if data_type:
            if isinstance(data_type, Iterable):  # pylint: disable=W1116

                data_type_req = [DATATYPE_MAP.get(data_type) for data_type in data_type]
            else:
                data_type_req = [DATATYPE_MAP.get(data_type)]
        else:
            data_type_req = []

        if isinstance(dataset, FusionDataset):
            dataset_client = self.get_or_create_fusion_dataset(
                dataset.name, dataset.is_continuous, data_type_req
            )
        else:
            dataset_client = self.get_or_create_dataset(
                dataset.name, dataset.is_continuous, data_type_req
            )

        if dataset.catalog:
            dataset_client.upload_catalog(dataset.catalog)

        for segment in dataset:
            dataset_client.upload_segment_object(
                segment,  # type: ignore[arg-type]
                jobs=jobs,
                skip_uploaded_files=skip_uploaded_files,
            )

        return dataset_client
