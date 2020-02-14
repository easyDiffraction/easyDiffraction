import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.QtInterface import QtCalculatorInterface,  ProjectDict

import PyImports.DisplayModels.BraggPeaksModel as Model

TEST_FILE = "file:Tests/Data/main.cif"


def test_BraggPeaksModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._headers_model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 89
    assert m._model.columnCount() == 4

    # assert m._tick_model.rowCount() == 665
    # assert m._tick_model.columnCount() == 2

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=Qt.DisplayRole) == 1
    assert m._model.item(0, 3).data(role=Qt.DisplayRole) == 9.596088259850408
    assert m._model.item(88, 0).data(role=Qt.DisplayRole) == 10
    assert m._model.item(88, 3).data(role=Qt.DisplayRole) == 82.01838528584905

    # assert m._tick_model.item(0, 0).data(role=Qt.DisplayRole) == 9.638782163644526
    # assert m._tick_model.item(0, 1).data(role=Qt.DisplayRole) == 0
    # assert m._tick_model.item(664, 0).data(role=Qt.DisplayRole) == 82.12103627681525
    # assert m._tick_model.item(664, 1).data(role=Qt.DisplayRole) == 6

    # test asModel
    assert m._model == m.asModel()
    # assert m._tick_model == m.asTickModel()

