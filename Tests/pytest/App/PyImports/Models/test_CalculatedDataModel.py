import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.Interface import CalculatorInterface

import PyImports.DisplayModels.CalculatedDataModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_CalculatedDataModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = CalculatorInterface(calculator)

    m = Model.CalculatedDataModel()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 381
    assert m._model.columnCount() == 4

    assert m._headers_model.rowCount() == 0
    assert m._headers_model.columnCount() == 0

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert m._model.item(0, 3).data(role=Qt.DisplayRole) == 438.3046174533981
    assert m._model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert m._model.item(380, 3).data(role=Qt.DisplayRole) == 58.024190593574644

    # test asModel
    assert m._model == m.asModel()
    assert m._headers_model == m.asHeadersModel()


def test_CalculatedDataModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.CalculatedDataModel()
        m.setCalculatorInterface(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
