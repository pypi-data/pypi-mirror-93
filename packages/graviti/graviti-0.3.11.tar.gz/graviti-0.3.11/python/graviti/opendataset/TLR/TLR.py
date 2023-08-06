#!/usr/bin/env python3
#
# Copytright 2020 Graviti. All Rights Reserved
#
# pylint: disable=invalid-name

"""This file defines Traffic Lights Recognition Dataloader"""

import os
from collections import defaultdict
from typing import Dict, List
from xml.dom.minidom import parse

from ...dataset import Data, Dataset
from ...label import LabeledBox2D, LabelType
from .._utility import glob

DATASET_NAME = "TLR"


def TLR(path: str) -> Dataset:
    """
    Load Traffic Lights Recognition to TensorBay

    :param path: the root directory of the dataset

    The file structure should like this:
    root_path/
        Lara3D_URbanSeq1_JPG/
            frame_011149.jpg
            frame_011150.jpg
            frame_<frame_index>.jpg
            ...
        Lara_UrbanSeq1_GroundTruth_cvml.xml
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog.json"))
    segment = dataset.create_segment()

    file_path_list = glob(os.path.join(root_path, "Lara3D_UrbanSeq1_JPG", "*.jpg"))
    labels = _parse_xml(os.path.join(root_path, "Lara_UrbanSeq1_GroundTruth_cvml.xml"))
    for file_path in file_path_list:
        # the image file name looks like:
        # frame_000001.jpg
        frame_index = int(os.path.basename(file_path)[6:-4])
        data = Data(file_path)
        data.register_label(LabelType.BOX2D)
        for label in labels[frame_index]:
            data.append_label(label)
        segment.append(data)
    return dataset


def _parse_xml(xml_path: str) -> Dict[int, List[LabeledBox2D]]:
    dom = parse(xml_path)
    frames = dom.documentElement.getElementsByTagName("frame")

    label_dict = defaultdict(list)

    for frame in frames:
        index = int(frame.getAttribute("number"))
        object_list = frame.getElementsByTagName("objectlist")[0]
        for obj in object_list.getElementsByTagName("object"):
            box = obj.getElementsByTagName("box")[0]
            box_h = int(box.getAttribute("h"))
            box_w = int(box.getAttribute("w"))
            box_xc = int(box.getAttribute("xc"))
            box_yc = int(box.getAttribute("yc"))

            label_dict[index].append(
                LabeledBox2D(
                    x=box_xc - box_w // 2,
                    y=box_yc - box_h // 2,
                    width=box_w,
                    height=box_h,
                    category=obj.getElementsByTagName("subtype")[0].firstChild.data,
                )
            )
    return label_dict
