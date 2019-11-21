import pytest
import os
import sys
from pytest_mock import mocker
from _pytest import monkeypatch
from pathlib import Path

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
    FILE = Path(saveName1).as_uri()
    isSaved, saveName2 = create_project_zip(data_dir, FILE)
    assert isSaved == True
    assert saveName1 == str(saveName2)
    assert os.path.isfile(saveName1) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    saveName1 = os.path.join(temp1.name, 'aa')
    saveName3 = saveName1 + '.zip'
    FILE = Path(saveName1).as_uri()
    isSaved, saveName2 = create_project_zip(data_dir, FILE)
    assert isSaved == True
    assert str(saveName2) == saveName3
    assert os.path.isfile(saveName3) == True
    temp1.cleanup()

    temp1 = make_temp_dir()
    FILE = Path(os.path.join(temp1.name, 'aa.zip')).as_uri()
    with pytest.raises(FileNotFoundError):
        isSaved, saveName2 = create_project_zip('Dummy/Dir', FILE)
    temp1.cleanup()
