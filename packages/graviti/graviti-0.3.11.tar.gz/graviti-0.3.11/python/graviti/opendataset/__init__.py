#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""OpenDataset dataloader collections."""

from .AnimalsWithAttributes2 import AnimalsWithAttributes2
from .BSTLD import BSTLD
from .CarConnection import CarConnection
from .CoinImage import CoinImage
from .DeepRoute import DeepRoute
from .DownsampledImagenet import DownsampledImagenet
from .Elpv import Elpv
from .Flower import Flower17, Flower102
from .FSDD import FSDD
from .HardHatWorkers import HardHatWorkers
from .HeadPoseImage import HeadPoseImage
from .ImageEmotion import ImageEmotionAbstract, ImageEmotionArtphoto
from .JHU_CROWD import JHU_CROWD
from .KenyanFood import KenyanFoodOrNonfood, KenyanFoodType
from .KylbergTexture import KylbergTexture
from .LeedsSportsPose import LeedsSportsPose
from .LISATrafficLight import LISATrafficLight
from .NeolixOD import NeolixOD
from .Newsgroups20 import Newsgroups20
from .THUCNews import THUCNews
from .TLR import TLR

__all__ = [
    "AnimalsWithAttributes2",
    "BSTLD",
    "CarConnection",
    "CoinImage",
    "DeepRoute",
    "DownsampledImagenet",
    "Elpv",
    "FSDD",
    "Flower102",
    "Flower17",
    "HardHatWorkers",
    "HeadPoseImage",
    "ImageEmotionAbstract",
    "ImageEmotionArtphoto",
    "JHU_CROWD",
    "KenyanFoodOrNonfood",
    "KenyanFoodType",
    "KylbergTexture",
    "LISATrafficLight",
    "LeedsSportsPose",
    "NeolixOD",
    "Newsgroups20",
    "THUCNews",
    "TLR",
]
