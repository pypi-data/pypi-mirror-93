#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file defines the Leeds Sports Pose Dataloader"""

import os

import numpy as np

from ...dataset import Data, Dataset
from ...geometry import Keypoint2D
from ...label import LabeledKeypoints2D, LabelType
from .._utility import glob

DATASET_NAME = "LeedsSportsPose"


def LeedsSportsPose(path: str) -> Dataset:
    """LeedsSportsPose open dataset dataloader.

    :param path: Path to LeedsSportsPose
    The folder structure should be like:
    <path>
        joints.mat
        images/
            im0001.jpg
            im0002.jpg
            ...
    :return: loaded LeedsSportsPose Dataset
    """
    from scipy.io import loadmat  # pylint: disable=import-outside-toplevel

    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog.json"))
    segment = dataset.create_segment()

    mat = loadmat(os.path.join(root_path, "joints.mat"))

    keypoints_list = np.transpose(mat["joints"])
    image_paths = glob(os.path.join(root_path, "images", "*.jpg"))
    for image_path in image_paths:
        data = Data(image_path)
        data.register_label(LabelType.KEYPOINTS2D)
        index = int(os.path.basename(image_path)[2:-4]) - 1  # get image index from "im0001.jpg"

        keypoints = LabeledKeypoints2D()
        for keypoint in keypoints_list[index]:
            keypoints.append(  # pylint: disable=no-member  # pylint issue #3131
                Keypoint2D(keypoint[0], keypoint[1], int(keypoint[2]))
            )

        data.append_label(keypoints)
        segment.append(data)
    return dataset
