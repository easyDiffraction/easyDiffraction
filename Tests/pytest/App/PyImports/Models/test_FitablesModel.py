import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.FitablesModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_FitablesModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.FitablesModel()
    m.setCalculatorInterface(calculator)

    assert isinstance(m._model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 34
    assert m._model.columnCount() == 1

    assert len(m._model.roleNames()) == len(m._roles_dict)
    assert b'path' in m._roles_dict.values()
    assert b'refine' in m._roles_dict.values()

    fr = Qt.UserRole + 1
    # Test stuff from _setModelFromProject here
    # first and last row
    assert m._model.item(0, 0).data(role=fr+1) == 'phases Fe3O4 cell length_a'
    assert m._model.item(0, 0).data(role=fr+2) == 8.57
    assert m._model.item(0, 0).data(role=fr+3) == 0.0
    assert m._model.item(0, 0).data(role=fr+4) == pytest.approx(6.856)
    assert m._model.item(0, 0).data(role=fr+5) == 10.284
    assert m._model.item(0, 0).data(role=fr+6) == True
    assert m._model.item(0, 0).data(role=fr+7) == None

    assert m._model.item(33, 0).data(role=fr+1) == 'experiments pnd resolution y'
    assert m._model.item(33, 0).data(role=fr+2) == 0.0
    assert m._model.item(33, 0).data(role=fr+3) == 0.0
    assert m._model.item(33, 0).data(role=fr+4) == 0.0
    assert m._model.item(33, 0).data(role=fr+5) == 0.0
    assert m._model.item(33, 0).data(role=fr+6) == False
    assert m._model.item(33, 0).data(role=fr+7) == None

    # test asModel
    assert m._model == m.asModel()


def test_FitablesModelModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.FitablesModel()
        m.setCalculatorInterface(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
