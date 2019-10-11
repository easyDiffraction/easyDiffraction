import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.CalculatedDataModel as Model

TEST_FILE = "file:Tests/Data/main.rcif"

def test_CalculatedDataModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.CalculatedDataModel(calculator)

    assert isinstance(m._data_model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    # assure _setModelFromProject got called
    assert m._data_model.rowCount() == 381
    assert m._data_model.columnCount() == 4

    assert m._headers_model.rowCount() == 0
    assert m._headers_model.columnCount() == 0

    # Test stuff from _setModelFromProject here
    assert m._data_model.item(0, 0).data(role=Qt.DisplayRole) == 4.0
    assert m._data_model.item(0, 3).data(role=Qt.DisplayRole) == pytest.approx(438.4046174)
    assert m._data_model.item(380, 0).data(role=Qt.DisplayRole) == 80.0
    assert m._data_model.item(380, 3).data(role=Qt.DisplayRole) == pytest.approx(58.4643675)

    # test asModel
    assert m._data_model == m.asDataModel()
    assert m._headers_model == m.asHeadersModel()


def test_CalculatedDataModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.CalculatedDataModel(calculator)

    # empty file
    file_path = QUrl("file:Tests/Data/Empty.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
