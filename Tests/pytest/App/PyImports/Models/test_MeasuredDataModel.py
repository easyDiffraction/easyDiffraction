import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Interface import CalculatorInterface

import PyImports.DisplayModels.MeasuredDataModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_MeasuredDataModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = CalculatorInterface(calculator)

    m = Model.MeasuredDataModel()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 381
    assert m._model.columnCount() == 7

    assert m._headers_model.rowCount() == 1
    assert m._headers_model.columnCount() == 7

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert m._model.item(0, 6).data(role=Qt.DisplayRole) == 585.055382546602
    assert m._model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert m._model.item(380, 6).data(role=Qt.DisplayRole) == 762.9590461224967

    assert m._headers_model.item(0, 0).data(role=Qt.DisplayRole) == 'x'
    assert m._headers_model.item(0, 1).data(role=Qt.DisplayRole) == 'y_obs_up'
    assert m._headers_model.item(0, 2).data(role=Qt.DisplayRole) == 'sy_obs_up'
    assert m._headers_model.item(0, 3).data(role=Qt.DisplayRole) == 'y_obs_down'
    assert m._headers_model.item(0, 4).data(role=Qt.DisplayRole) == 'sy_obs_down'
    assert m._headers_model.item(0, 5).data(role=Qt.DisplayRole) == 'y_obs_upper'
    assert m._headers_model.item(0, 6).data(role=Qt.DisplayRole) == 'y_obs_lower'

    # test asModel
    assert m._model == m.asModel()
    assert m._headers_model == m.asHeadersModel()


def test_MeasuredDataModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.MeasuredDataModel()
        m.setCalculatorInterface(calculator)
