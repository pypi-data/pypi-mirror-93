#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines common_loads method"""

from typing import Any, Type, TypeVar

_T = TypeVar("_T")


def common_loads(object_class: Type[_T], loads: Any) -> _T:
    """A common method for loading an object from a dict or list of dict.

    :param object_class: The class of the object to be loaded
    :param loads: The information of the object in a dict or a list of dict
    :return: The loaded object
    """
    obj: _T = object.__new__(object_class)
    obj._loads(loads)  # type: ignore[attr-defined]  # pylint: disable=protected-access
    return obj
