import sys
import os
import webbrowser

import pytest
from pytest_mock import mocker
from _pytest import monkeypatch

from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl

# tested module
from PyImports.Helpers import *

def test_nested_get():
    dictionary = {}
    key_list = []

    assert nested_get(dictionary, key_list) == {}

    dictionary = {1:'a', 2:'b'}
    key_list = [1,2]

    assert nested_get(dictionary, key_list) == ""


def test_nested_set():
    dictionary = {}
    key_list = []
    value = 1.0

    with pytest.raises(IndexError):
        nested_set(dictionary, key_list, value)

    dictionary = {1:'a', 2:'b', 3:'c'}
    key_list = [1]

    assert nested_get(dictionary, key_list) == "a"

def no_test_find_in_obj():
    obj = QObject
    condition = 1
    path = ""

    assert list(find_in_obj(obj, condition, path=path)) == ""

    obj = {}
    condition = 1
    path = ""

    assert list(find_in_obj(obj, condition, path=path)) == ""

    obj = {1:'a', 2:'b', 3:'c'}
    condition = 1
    path = ""

    assert list(find_in_obj(obj, condition, path=path)) == ""

def test_open_url(mocker):
    mocker.patch('logging.info')

    # bad open
    url = None
    open_url(url)
    bad_msg = 'Report viewing failed: _getfullpathname: path should be string, bytes or os.PathLike, not NoneType'
    logging.info.assert_called_once_with(bad_msg)

    url = {}
    open_url(url)
    bad_msg = 'Report viewing failed: _getfullpathname: path should be string, bytes or os.PathLike, not dict'
    logging.info.assert_called_with(bad_msg)

    mocker.patch('webbrowser.open')
    # good open
    url = "test.html"
    open_url(url)

    # can't test the string passed since it is strictly machine dependent
    webbrowser.open.assert_called_once()


