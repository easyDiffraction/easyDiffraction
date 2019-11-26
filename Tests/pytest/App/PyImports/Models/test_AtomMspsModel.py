import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.AtomMspsModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_AtomMspsModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.AtomMspsModel()
    m.setCalculator(calculator)

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    assert m._label_role == 257
    assert m._chi23_role == 265

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 3
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data() == 'Fe3A'
    assert m._model.item(0, 0).data(role=m._type_role) == 'cani'
    assert m._model.item(0, 0).data(role=m._chiiso_role) == ''
    assert m._model.item(0, 0).data(role=m._chi11_role) == -0.5
    assert m._model.item(0, 0).data(role=m._chi22_role) == -0.5
    assert m._model.item(0, 0).data(role=m._chi33_role) == -0.5
    assert m._model.item(0, 0).data(role=m._chi12_role) == 0.0
    assert m._model.item(0, 0).data(role=m._chi13_role) == 0.0
    assert m._model.item(0, 0).data(role=m._chi23_role) == 0.0

    assert m._model.item(1, 0).data() == 'Fe3B'
    assert m._model.item(1, 0).data(role=m._type_role) == 'cani'
    assert m._model.item(1, 0).data(role=m._chiiso_role) == ''
    assert m._model.item(1, 0).data(role=m._chi11_role) == 0.2
    assert m._model.item(1, 0).data(role=m._chi22_role) == 0.2
    assert m._model.item(1, 0).data(role=m._chi33_role) == 0.2
    assert m._model.item(1, 0).data(role=m._chi12_role) == 0.0
    assert m._model.item(1, 0).data(role=m._chi13_role) == 0.0
    assert m._model.item(1, 0).data(role=m._chi23_role) == 0.0

    assert m._model.item(2, 0).data() == 'O1'
    assert m._model.item(2, 0).data(role=m._type_role) == ''
    assert m._model.item(2, 0).data(role=m._chi11_role) == ''
    assert m._model.item(2, 0).data(role=m._chi11_role) == ''
    assert m._model.item(2, 0).data(role=m._chi22_role) == ''
    assert m._model.item(2, 0).data(role=m._chi33_role) == ''
    assert m._model.item(2, 0).data(role=m._chi12_role) == ''
    assert m._model.item(2, 0).data(role=m._chi13_role) == ''
    assert m._model.item(2, 0).data(role=m._chi23_role) == ''

    # test asModel
    assert m._model == m.asModel()

def test_AtomMspsModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.AtomMspsModel()
        m.setCalculator(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
