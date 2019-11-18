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

    dictionary = {1: 'a', 2: 'b'}
    key_list = [1, 2]

    assert nested_get(dictionary, key_list) == ""


def test_nested_set():
    dictionary = {}
    key_list = []
    value = 1.0

    with pytest.raises(IndexError):
        nested_set(dictionary, key_list, value)

    dictionary = {1: 'a', 2: 'b', 3: 'c'}
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

    obj = {1: 'a', 2: 'b', 3: 'c'}
    condition = 1
    path = ""

    assert list(find_in_obj(obj, condition, path=path)) == ""


def test_open_url(mocker):
    mocker.patch('logging.info')

    # bad open
    url = None
    open_url(url)
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        bad_msg = 'Report viewing failed: expected str, bytes or os.PathLike object, not NoneType'
    else:
        bad_msg = 'Report viewing failed: _getfullpathname: path should be string, bytes or os.PathLike, not NoneType'
    logging.info.assert_called_once_with(bad_msg)

    url = {}
    open_url(url)
    open_url(url)
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        bad_msg = 'Report viewing failed: expected str, bytes or os.PathLike object, not dict'
    else:
        bad_msg = 'Report viewing failed: _getfullpathname: path should be string, bytes or os.PathLike, not dict'
    logging.info.assert_called_with(bad_msg)

    mocker.patch('webbrowser.open')
    # good open
    url = "test.html"
    open_url(url)

    # can't test the string passed since it is strictly machine dependent
    webbrowser.open.assert_called_once()


def test_get_num_refine_pars():
    obj = {'a': {'b': 1,
                 'refine': True,
                 'hide': False
                 },
           'c': {'d': 3,
                 'e': 4,
                 'refine': False,
                 'hide': False
                 },
           'f': {'g': 5,
                 'refine': True,
                 'hide': False
                 },
           'h': {'i': 6,
                 'refine': True,
                 'hide': True
                 }
           }
    numPars = get_num_refine_pars(obj)
    expectedPars = 2
    assert numPars == expectedPars


def test_check_project_dict():
    dict1 = {'a': 1,
             'b': 2,
             'phases': 3}
    dict2 = {
        'phases': [],
        'experiments': [],
        'calculations': []
    }
    dict3 = {
        'phases': 1,
        'experiments': 2,
        'calculations': 3
    }

    assert check_project_dict(dict1) == False
    assert check_project_dict(dict2) == False
    assert check_project_dict(dict3) == True


def validate_URI(file_uri, expected_windows_path, expected_posix_path):
    if expected_windows_path is not None:
        expected_windows_path_object = pathlib.PureWindowsPath(expected_windows_path)
    if expected_posix_path is not None:
        expected_posix_path_object = pathlib.PurePosixPath(expected_posix_path)

    if expected_windows_path is not None:
        if os.name == "nt":
            assert file_uri_to_path(file_uri) == expected_windows_path_object
        assert file_uri_to_path(file_uri, pathlib.PureWindowsPath) == expected_windows_path_object

    if expected_posix_path is not None:
        if os.name != "nt":
            assert file_uri_to_path(file_uri) == expected_posix_path_object
        assert file_uri_to_path(file_uri, pathlib.PurePosixPath) == expected_posix_path_object


def test_URI_some_paths():
    validate_URI(pathlib.PureWindowsPath(r"C:\Windows\System32\Drivers\etc\hosts").as_uri(),
                 expected_windows_path=r"C:\Windows\System32\Drivers\etc\hosts",
                 expected_posix_path=r"/C:/Windows/System32/Drivers/etc/hosts")

    validate_URI(pathlib.PurePosixPath(r"/C:/Windows/System32/Drivers/etc/hosts").as_uri(),
                 expected_windows_path=r"C:\Windows\System32\Drivers\etc\hosts",
                 expected_posix_path=r"/C:/Windows/System32/Drivers/etc/hosts")

    validate_URI(pathlib.PureWindowsPath(r"C:\some dir\some file").as_uri(),
                 expected_windows_path=r"C:\some dir\some file",
                 expected_posix_path=r"/C:/some dir/some file")

    validate_URI(pathlib.PurePosixPath(r"/C:/some dir/some file").as_uri(),
                 expected_windows_path=r"C:\some dir\some file",
                 expected_posix_path=r"/C:/some dir/some file")


def test_invalid_URI_url():
    with pytest.raises(ValueError) as excinfo:
        validate_URI(r"file://C:/test/doc.txt",
                     expected_windows_path=r"test\doc.txt",
                     expected_posix_path=r"/test/doc.txt")
        assert "is not absolute" in str(excinfo.value)


def test_URI_escaped():
    validate_URI(r"file:///home/user/some%20file.txt",
                 expected_windows_path=None,
                 expected_posix_path=r"/home/user/some file.txt")
    validate_URI(r"file:///C:/some%20dir/some%20file.txt",
                 expected_windows_path="C:\some dir\some file.txt",
                 expected_posix_path=r"/C:/some dir/some file.txt")


def test_no_URI_authority():
    validate_URI(r"file:c:/path/to/file",
                 expected_windows_path=r"c:\path\to\file",
                 expected_posix_path=None)
    validate_URI(r"file:/path/to/file",
                 expected_windows_path=None,
                 expected_posix_path=r"/path/to/file")
