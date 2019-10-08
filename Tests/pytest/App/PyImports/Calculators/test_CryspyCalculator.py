import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

import cryspy

# module for testing
from PyImports.Calculators.CryspyCalculator import CryspyCalculator

TEST_FILE = "file:Tests/Data/main.rcif"

@pytest.fixture
def cal():
    file_path = QUrl(TEST_FILE).toLocalFile()
    calc = CryspyCalculator(file_path)
    return calc

def test_init(cal):
    # initial state of the object
    assert len(cal._app_dict) == 3
    assert len(cal._calculations_dict) == 1
    assert len(cal._info_dict) == 7
    assert len(cal._phases_dict) == 1
    assert len(cal._experiments_dict) == 1
    assert len(cal._calculations_dict) == 1

    assert cal._main_rcif_path == TEST_FILE.replace('file:','')

    assert len(cal._project_dict) == 6

def test_setAppDict(cal):

    assert 'name' in cal._app_dict.keys()
    assert cal._app_dict['name'] == 'easyDiffraction'
    assert 'version' in cal._app_dict.keys()
    assert 'url' in cal._app_dict.keys()

def test_setCalculatorDict(cal):

    assert 'name' in cal._calculator_dict.keys()
    assert cal._calculator_dict['name'] == 'CrysPy'
    assert 'version' in cal._calculator_dict.keys()
    assert 'url' in cal._calculator_dict.keys()

def test_setInfoDict(cal):

    assert len(cal._info_dict) == 7
    assert 'name' in cal._info_dict.keys()
    assert cal._info_dict['name'] == 'Fe3O4'
    assert 'refinement_datetime' in cal._info_dict.keys()
    assert 'experiment_ids' in cal._info_dict.keys()


def test_setPhasesDictFromCryspyObj(cal):
    # difficult test for creation of the phases dict
    cal._phases_dict.clear() # enforce
    assert cal._cryspy_obj.crystals != None

    cal.setPhasesDictFromCryspyObj()

    assert len(cal._phases_dict) == 1
    assert len(cal._phases_dict['Fe3O4']) == 4
    assert len(cal._phases_dict['Fe3O4']['cell']) == 6
    assert cal._phases_dict['Fe3O4']['cell']['length_a']['value'] == 8.57
    assert cal._phases_dict['Fe3O4']['cell']['length_b']['hide'] == True
    assert cal._phases_dict['Fe3O4']['cell']['length_c']['max'] == 1.2
    assert cal._phases_dict['Fe3O4']['cell']['angle_beta']['error'] == 0.0
    assert cal._phases_dict['Fe3O4']['cell']['angle_gamma']['constraint'] == None

    assert len(cal._phases_dict['Fe3O4']['space_group']) == 4
    assert cal._phases_dict['Fe3O4']['space_group']['crystal_system'] == 'mm'
    assert cal._phases_dict['Fe3O4']['space_group']['origin_choice'] == 'mm'

