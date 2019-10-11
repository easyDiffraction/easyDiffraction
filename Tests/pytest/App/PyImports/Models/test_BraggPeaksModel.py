import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.BraggPeaksModel as Model

TEST_FILE = "file:Tests/Data/main.rcif"

def test_BraggPeaksModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.BraggPeaksModel(calculator)

    assert isinstance(m._data_model, QStandardItemModel)
    assert isinstance(m._tick_model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    # assure _setModelFromProject got called
    assert m._data_model.rowCount() == 95
    assert m._data_model.columnCount() == 4

    assert m._tick_model.rowCount() == 665
    assert m._tick_model.columnCount() == 2

    # Test stuff from _setModelFromProject here
    assert m._data_model.item(0, 0).data(role=Qt.DisplayRole) == 1
    assert m._data_model.item(0, 3).data(role=Qt.DisplayRole) == 9.638782163644526
    assert m._data_model.item(94, 0).data(role=Qt.DisplayRole) == 12
    assert m._data_model.item(94, 3).data(role=Qt.DisplayRole) == 82.12103627681525

    assert m._tick_model.item(0, 0).data(role=Qt.DisplayRole) == 9.638782163644526
    assert m._tick_model.item(0, 1).data(role=Qt.DisplayRole) == 0
    assert m._tick_model.item(664, 0).data(role=Qt.DisplayRole) == 82.12103627681525
    assert m._tick_model.item(664, 1).data(role=Qt.DisplayRole) == 6

    # test asModel
    assert m._data_model == m.asDataModel()
    assert m._tick_model == m.asTickModel()

def test_BraggPeaksModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.BraggPeaksModel(calculator)

    # empty file
    file_path = QUrl("file:Tests/Data/Empty.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
