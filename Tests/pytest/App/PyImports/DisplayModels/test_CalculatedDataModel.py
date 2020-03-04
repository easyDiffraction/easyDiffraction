import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from PyImports.QtInterface import QtCalculatorInterface, ProjectDict

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
    assert m._model.columnCount() == 4

    assert m._headers_model.rowCount() == 1
    assert m._headers_model.columnCount() == 4

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert pytest.approx(m._model.item(0, 3).data(role=Qt.DisplayRole), 438.3046174533981)
    assert m._model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert pytest.approx(m._model.item(380, 3).data(role=Qt.DisplayRole), -58.83263649312255)

    # test asModel
    assert m._model == m.asModel()
    assert m._headers_model == m.asHeadersModel()

