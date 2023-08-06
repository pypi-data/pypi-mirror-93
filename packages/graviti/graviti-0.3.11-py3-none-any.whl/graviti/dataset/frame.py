#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Frame."""

from typing import Any, Dict, Optional, Sequence, Type, TypeVar

from ..geometry import Quaternion, Transform3D
from ..utility import UserMutableMapping, common_loads
from .data import Data


class Frame(UserMutableMapping[str, Data]):
    """This class defines the concept of frame,
    which represents a series of Data corresponding to different sensors.
    """

    _T = TypeVar("_T", bound="Frame")

    def __init__(self) -> None:
        self._data: Dict[str, Data] = {}
        self._pose: Optional[Transform3D] = None

    @classmethod
    def loads(cls: Type[_T], loads: Dict[str, Any]) -> _T:
        """Load a Frame from a dict containing the information.

        :param loads: A dict containing the information of a Frame
        {
            "pose": {
                "translation": {
                    "x":
                    "y":
                    "z":
                },
                "rotation": {
                    "w":
                    "x":
                    "y":
                    "z":
                },
            },
            "frame": {
                <key>: data_dict{...},
                <key>: data_dict{...},
                ...
                ...
            }
        }
        :return: The loaded Frame
        """
        return common_loads(cls, loads)

    def _loads(self, loads: Dict[str, Any]) -> None:
        self._data = {}
        for sensor, data_dict in loads["frame"].items():
            self._data[sensor] = Data.loads(data_dict)
        pose = loads.get("pose")
        self._pose = Transform3D.loads(pose) if pose else None

    def dumps(self) -> Dict[str, Any]:
        """dump a Frame into a frame_dict"""

        frame_dict: Dict[str, Any] = {}
        if self._pose:
            frame_dict["pose"] = self._pose.dumps()

        content_dict = {}
        for sensor, data in self._data.items():
            content_dict[sensor] = data.dumps()
        frame_dict["frame"] = content_dict

        return frame_dict

    @property
    def pose(self) -> Optional[Transform3D]:
        """Get the pose of the frame.

        :return: A Transform3D class object representing the pose of the frame
        """
        return self._pose

    def set_pose(
        self,
        transform: Transform3D.TransformType = None,
        *,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the pose of the current frame
        :param transform: A Transform3D object or a 4x4 or 3x4 transfrom matrix
        :param translation: Translation in a sequence of [x, y, z]
        :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or Quaternion
        :param loads: A dictionary containing the translation and the rotation
        :param kwargs: Other parameters to initialize rotation of the transform
        """
        if loads:
            self._pose = Transform3D.loads(loads)
            return

        self._pose = Transform3D(transform, translation=translation, rotation=rotation, **kwargs)
