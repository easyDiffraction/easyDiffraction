import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.QtInterface import QtCalculatorInterface,  ProjectDict

import PyImports.DisplayModels.FitablesModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_FitablesModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 22
    assert m._model.columnCount() == 1

    assert len(m._model.roleNames()) == len(m._roles_dict)
    assert b'path' in m._roles_dict.values()
    assert b'refine' in m._roles_dict.values()

    fr = Qt.UserRole + 1
    # Test stuff from _setModelFromProject here
    # first and last row
    assert m._model.item(0, 0).data(role=fr+1) == 'phases Fe3O4 cell length_a'
    assert m._model.item(0, 0).data(role=fr+2) == 8.36212
    assert m._model.item(0, 0).data(role=fr+3) == 0.0
    assert m._model.item(0, 0).data(role=fr+4) == pytest.approx(6.68969)
    assert m._model.item(0, 0).data(role=fr+5) == 10.034544
    assert m._model.item(0, 0).data(role=fr+6) is True
    assert m._model.item(0, 0).data(role=fr+7) == 'ang'

    assert m._model.item(21, 0).data(role=fr+1) == 'experiments pd resolution y'
    assert m._model.item(21, 0).data(role=fr+2) == 0.0
    assert m._model.item(21, 0).data(role=fr+3) == 0.0
    assert m._model.item(21, 0).data(role=fr+4) == 0.0
    assert m._model.item(21, 0).data(role=fr+5) == 0.0
    assert m._model.item(21, 0).data(role=fr+6) is False
    assert m._model.item(21, 0).data(role=fr+7) == ''

    # test asModel
    assert m._model == m.asModel()
