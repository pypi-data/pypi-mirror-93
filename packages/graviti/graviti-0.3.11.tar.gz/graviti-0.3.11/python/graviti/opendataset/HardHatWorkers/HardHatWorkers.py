#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define the Hard Hat Workers Dataloader"""

import os
from typing import Generator
from xml.etree import ElementTree

from ...dataset import Data, Dataset
from ...label import LabeledBox2D, LabelType
from .._utility import glob

DATASET_NAME = "Hard Hat Workers"


def HardHatWorkers(path: str) -> Dataset:
    """Load the Hard Hat Workers Dataset to TensorBay

    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        annotations/
            hard_hat_workers0.xml
            ...
        images/
            hard_hat_workers0.png
            ...

    :return: a loaded dataset
    """
    dataset = Dataset(DATASET_NAME)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog.json"))
    segment = dataset.create_segment()
    image_paths = glob(os.path.join(path, "images", "*.png"))
    for image_path in image_paths:
        data = Data(image_path)
        data.register_label(LabelType.BOX2D)
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        labels = _load_labels(os.path.join(path, "annotations", file_name + ".xml"))
        for label in labels:
            data.append_label(label)
        segment.append(data)
    return dataset


def _load_labels(label_file: str) -> Generator[LabeledBox2D, None, None]:
    label_tree = ElementTree.parse(label_file)
    for obj in label_tree.findall("object"):
        bndbox = obj.find("bndbox")
        box = (int(child.text) for child in bndbox)  # type: ignore[arg-type, union-attr]
        yield LabeledBox2D(box, category=obj.find("name").text)  # type: ignore[union-attr]
