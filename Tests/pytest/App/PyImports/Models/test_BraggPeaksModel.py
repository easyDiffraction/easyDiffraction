import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.Interface import CalculatorInterface

import PyImports.DisplayModels.BraggPeaksModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_BraggPeaksModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = CalculatorInterface(calculator)

    m = Model.BraggPeaksModel()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._tick_model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 95
    assert m._model.columnCount() == 4

    assert m._tick_model.rowCount() == 665
    assert m._tick_model.columnCount() == 2

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 1
    assert m._model.item(0, 3).data(role=Qt.DisplayRole) == 9.638782163644526
    assert m._model.item(94, 0).data(role=Qt.DisplayRole) == 12
    assert m._model.item(94, 3).data(role=Qt.DisplayRole) == 82.12103627681525

    assert m._tick_model.item(0, 0).data(role=Qt.DisplayRole) == 9.638782163644526
    assert m._tick_model.item(0, 1).data(role=Qt.DisplayRole) == 0
    assert m._tick_model.item(664, 0).data(role=Qt.DisplayRole) == 82.12103627681525
    assert m._tick_model.item(664, 1).data(role=Qt.DisplayRole) == 6

    # test asModel
    assert m._model == m.asModel()
    assert m._tick_model == m.asTickModel()

def test_BraggPeaksModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.BraggPeaksModel()
        m.setCalculatorInterface(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
