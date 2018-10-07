# -*- coding: utf-8 -*-
#
from __future__ import absolute_import

import os
import sys


def is_frozen():
    """
    :return: True if the executable is currently frozen
    """
    return getattr(sys, 'frozen', False)


def _resource_path_frozen(relative_path):
    """
    :return: PyInstaller frozen path to resource
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def _resource_path_dev(relative_path):
    """
    :return: Package relative path to resource
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    return _resource_path_frozen(relative_path) if is_frozen() else _resource_path_dev(relative_path)





