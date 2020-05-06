import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from PyImports.QtInterface import QtCalculatorInterface, ProjectDict

from PyImports.QtInterface import QtCalculatorInterface
import PyImports.DisplayModels.CalculatedDataModel as Model

TEST_FILE = "file:Tests/Data/main.cif"


def test_CalculatedDataModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 381
    assert m._model.columnCount() == 8

    assert m._headers_model.rowCount() == 1
    assert m._headers_model.columnCount() == 8

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert pytest.approx(m._model.item(0, 3).data(role=Qt.DisplayRole), 438.3046174533981)
    assert m._model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert pytest.approx(m._model.item(380, 3).data(role=Qt.DisplayRole), -58.83263649312255)

    # test asModel
    assert m._model == m.asModel()
    assert m._headers_model == m.asHeadersModel()

def test__yMax():
    m = Model()
    assert m._yMax() == 1
    m._setYMax(2)
    assert m._yMax() == 2
    m._setYMax(-99.99)
    assert m._yMax() == -99.99

def test__yMin():
    m = Model()
    assert m._yMin() == 0
    m._setYMin(2)
    assert m._yMin() == 2
    m._setYMin(-99.99)
    assert m._yMin() == -99.99

def test__yDiffMax():
    m = Model()
    assert m._yDiffMax() == 1
    m._setYDiffMax(2)
    assert m._yDiffMax() == 2
    m._setYDiffMax(-99.99)
    assert m._yDiffMax() == -99.99

def test__yDiffMin():
    m = Model()
    assert m._yDiffMin() == 0
    m._setYDiffMin(2)
    assert m._yDiffMin() == 2
    m._setYDiffMin(-99.99)
    assert m._yDiffMin() == -99.99

def test_setDataType():
    m = Model()
    assert m._y_calc_name == "y_calc_sum"
    assert m._y_obs_name == "y_obs"
    assert m._sy_obs_name == "sy_obs"
    m.setDataType("Boom")
    assert m._y_calc_name == "y_calc_sum"
    assert m._y_obs_name == "y_obs"
    assert m._sy_obs_name == "sy_obs"
    m.setDataType("Sum")
    assert m._y_calc_name == "y_calc_sum"
    assert m._y_obs_name == "y_obs"
    assert m._sy_obs_name == "sy_obs"
    m.setDataType("Difference")
    assert m._y_calc_name == "y_calc_diff"
    assert m._y_obs_name == "y_obs_diff"
    assert m._sy_obs_name == "sy_obs_diff"
    m.setDataType("Up")
    assert m._y_calc_name == "y_calc_up"
    assert m._y_obs_name == "y_obs_up"
    assert m._sy_obs_name == "sy_obs_up"
    m.setDataType("Down")
    assert m._y_calc_name == "y_calc_down"
    assert m._y_obs_name == "y_obs_down"
    assert m._sy_obs_name == "sy_obs_down"
