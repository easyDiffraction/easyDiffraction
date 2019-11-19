import pytest
import os
from pytest_mock import mocker
from _pytest import monkeypatch

from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl

# tested module
from PyImports.ProjectIO import *


TEST_ZIP = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project.zip')
TEST_ZIP_ERROR = os.path.join(os.getcwd(), 'Tests', 'Data', 'Fe3O4_project_error.zip')
TEST_CIF = os.path.join(os.getcwd(), 'Tests', 'Data', 'main.cif')


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


def test_check_if_zip():
    assert check_if_zip(TEST_ZIP) == True
    assert check_if_zip(TEST_CIF) == False


def test_check_project_file():

    assert check_project_file(TEST_ZIP) == True
    assert check_project_file(TEST_ZIP_ERROR) == False
    with pytest.raises(TypeError):
        err = check_project_file(TEST_CIF)


def test_make_temp_dir():
    folder = make_temp_dir()
    assert os.path.exists(folder.name) == True
    folder.cleanup()
    assert os.path.exists(folder.name) == False


def test_temp_project_dir():
    folder = temp_project_dir(TEST_ZIP)
    files = ['main.cif', 'phases.cif', 'experiments.cif']
    for file in files:
        assert os.path.isfile(os.path.join(folder.name, file)) == True
    folder.cleanup()

def test_create_project_zip():
    data_dir = 'Tests/Data/'

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa.zip')
    isSaved, saveName2 = create_project_zip(data_dir, saveName1)
    assert isSaved == True
    assert saveName1 == str(saveName2)
    assert os.path.isfile(saveName1) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa')
    saveName3 = saveName1 + '.zip'
    isSaved, saveName2 = create_project_zip(data_dir, saveName1)
    assert isSaved == True
    assert str(saveName2) == saveName3
    assert os.path.isfile(saveName3) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa.zip')
    with pytest.raises(FileNotFoundError):
        create_project_zip('Dummy/Dir', saveName1)
    temp1.cleanup()


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
