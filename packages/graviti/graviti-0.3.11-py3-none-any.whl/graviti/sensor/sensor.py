#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class SensorType, Sensor, Lidar, Radar, Camera and FisheyeCamera."""

from typing import Any, Dict, Optional, Sequence, Type, TypeVar, Union

from ..geometry import Quaternion, Transform3D
from ..utility import NameClass, ReprType, TypeClass, TypeEnum, TypeRegister, common_loads
from .intrinsics import CameraIntrinsics

_T = TypeVar("_T", bound="Sensor")


class SensorType(TypeEnum):
    """this class defines the type of the sensors.

    :param sensor_name: The name string of the json format sensor
    """

    LIDAR = "LIDAR"
    RADAR = "RADAR"
    CAMERA = "CAMERA"
    FISHEYE_CAMERA = "FISHEYE_CAMERA"


class Sensor(NameClass, TypeClass[SensorType]):
    """A class representing sensor including
    name, description, translation and rotation.

    :param name: A string representing the sensor's name
    :raises
        TypeError: Can't instantiate abstract class Sensor
    """

    _repr_type = ReprType.INSTANCE
    _repr_attributes = ("extrinsics",)
    _repr_maxlevel = 3

    def __new__(
        cls: Type[_T],
        name: str,  # pylint: disable=unused-argument
    ) -> _T:
        if cls is Sensor:
            raise TypeError("Can't instantiate abstract class Sensor")

        obj: _T = object.__new__(cls)
        return obj

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._extrinsics: Optional[Transform3D] = None

    @classmethod
    def loads(cls: Type[_T], loads: Dict[str, Any]) -> _T:
        """Load a Sensor from a dict containing the information.

        :loads: A dictionary containing name, description and sensor extrinsics
        :return: The loaded Sensor
        """
        sensor: _T = common_loads(SensorType(loads["type"]).type, loads)
        return sensor

    def _loads(self, loads: Dict[str, Any]) -> None:
        super()._loads(loads)
        extrinsics = loads.get("extrinsics")
        if extrinsics:
            self._extrinsics = Transform3D.loads(extrinsics)
        else:
            self._extrinsics = None

    def dumps(self) -> Dict[str, Any]:
        """Dumps the sensor as a dictionary.

        :return: A dictionary containing name, description and extrinsics
        """
        data: Dict[str, Any] = super().dumps()
        data["type"] = self.enum.value
        if self._extrinsics:
            data["extrinsics"] = self._extrinsics.dumps()

        return data

    @property
    def extrinsics(self) -> Optional[Transform3D]:
        """Return extrinsics of the sensor.

        :return: Extrinsics of the sensor
        """
        return self._extrinsics

    def set_extrinsics(
        self,
        transform: Transform3D.TransformType = None,
        *,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the extrinsics of the sensor.

        :param transform: A Transform3D object representing the extrinsics
        :param translation: Translation in a sequence of [x, y, z]
        :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or Quaternion
        :param loads: A dictionary containing the translation and the rotation
        :param matrix: A 4x4 transform matrix
        :param kwargs: Other parameters to initialize rotation
        """
        if loads:
            self._extrinsics = Transform3D.loads(loads)
            return

        self._extrinsics = Transform3D(
            transform, translation=translation, rotation=rotation, **kwargs
        )

    def set_translation(
        self,
        *args: Union[float, Sequence[float]],
        **kwargs: float,
    ) -> None:
        """Set the translation of the sensor.

        :param args: Coordinates of the translation vector
        :param kwargs: keyword-only argument to set different dimension for translation vector
            sensor.set_translation(x=1, y=2, z=3)
        """
        if not self._extrinsics:
            self._extrinsics = Transform3D()
        self._extrinsics.set_translation(*args, **kwargs)

    def set_rotation(
        self,
        *args: Union[Quaternion.ArgsType, float],
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the rotation of the sensor.

        :param args: Coordinates of the Quaternion
        :param kwargs: keyword-only argument to the Quaternion
        """
        if not self._extrinsics:
            self._extrinsics = Transform3D()
        self._extrinsics.set_rotation(*args, **kwargs)


@TypeRegister(SensorType.LIDAR)
class Lidar(Sensor):
    """This class defines the concept of lidar."""


@TypeRegister(SensorType.RADAR)
class Radar(Sensor):
    """This class defines the concept of radar."""


@TypeRegister(SensorType.CAMERA)
class Camera(Sensor):
    """A class representing camera including
    name, description, translation , rotation, cameraMatrix and distortionCoefficients.

    :param name: A string representing camera's name
    """

    _repr_attributes = Sensor._repr_attributes + ("intrinsics",)  # type: ignore[assignment]
    _T = TypeVar("_T", bound="Camera")

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._intrinsics: Optional[CameraIntrinsics] = None

    @classmethod
    def loads(cls: Type[_T], loads: Dict[str, Any]) -> _T:
        """Load a Camera from a dict containing the information of the camera.

        :param loads: A dictionary containing name, description, extrinsics and intrinsics
        :return: The loaded Camera
        """
        return common_loads(cls, loads)

    def _loads(self, loads: Dict[str, Any]) -> None:
        super()._loads(loads)
        self._intrinsics = CameraIntrinsics.loads(loads["intrinsics"])

    def dumps(self) -> Dict[str, Any]:
        """Dumps the camera as a dictionary.

        :return: A dictionary containing name, description, extrinsics and intrinsics
        """
        message = super().dumps()
        if self._intrinsics:
            message["intrinsics"] = self._intrinsics.dumps()
        return message

    @property
    def intrinsics(self) -> Optional[CameraIntrinsics]:
        """Return intrinsics."""

        return self._intrinsics

    def set_camera_matrix(
        self,
        matrix: Optional[Sequence[Sequence[float]]] = None,
        **kwargs: float,
    ) -> None:
        """Set camera matrix."""

        if not self._intrinsics:
            self._intrinsics = CameraIntrinsics(matrix, _init_distortion=False, **kwargs)
            return

        self._intrinsics.set_camera_matrix(matrix, **kwargs)

    def set_distortion_coefficients(self, **kwargs: float) -> None:
        """Set distortion coefficients.
        :raise VauleError: When camera matrix of intrinsics is not set yet.
        """

        if not self._intrinsics:
            raise ValueError("Camera matrix of camera intrinsics must be set first.")
        self._intrinsics.set_distortion_coefficients(**kwargs)


@TypeRegister(SensorType.FISHEYE_CAMERA)
class FisheyeCamera(Camera):
    """This class defines the concept of fisheye camera."""
