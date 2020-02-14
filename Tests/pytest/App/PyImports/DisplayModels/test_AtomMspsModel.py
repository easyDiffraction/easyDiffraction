import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.QtInterface import QtCalculatorInterface,  ProjectDict

import PyImports.DisplayModels.AtomMspsModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_AtomMspsModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    assert m._label_role == 257
    assert m._chi23_role == 265

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 3
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data() == 'Fe3A'
    assert m._model.item(0, 0).data(role=m._type_role) == 'Cani'
    assert m._model.item(0, 0).data(role=m._chiiso_role) == ''
    assert m._model.item(0, 0).data(role=m._chi11_role) == -3.468
    assert m._model.item(0, 0).data(role=m._chi22_role) == -3.468
    assert m._model.item(0, 0).data(role=m._chi33_role) == -3.468
    assert m._model.item(0, 0).data(role=m._chi12_role) == 0.0
    assert m._model.item(0, 0).data(role=m._chi13_role) == 0.0
    assert m._model.item(0, 0).data(role=m._chi23_role) == 0.0

    assert m._model.item(1, 0).data() == 'Fe3B'
    assert m._model.item(1, 0).data(role=m._type_role) == 'Cani'
    assert m._model.item(1, 0).data(role=m._chiiso_role) == ''
    assert m._model.item(1, 0).data(role=m._chi11_role) == 3.041
    assert m._model.item(1, 0).data(role=m._chi22_role) == 3.041
    assert m._model.item(1, 0).data(role=m._chi33_role) == 3.041
    assert m._model.item(1, 0).data(role=m._chi12_role) == 0.0
    assert m._model.item(1, 0).data(role=m._chi13_role) == 0.0
    assert m._model.item(1, 0).data(role=m._chi23_role) == 0.0

    assert m._model.item(2, 0).data() == 'O'
    assert m._model.item(2, 0).data(role=m._type_role) is None
    assert m._model.item(2, 0).data(role=m._chi11_role) is None
    assert m._model.item(2, 0).data(role=m._chi11_role) is None
    assert m._model.item(2, 0).data(role=m._chi22_role) is None
    assert m._model.item(2, 0).data(role=m._chi33_role) is None
    assert m._model.item(2, 0).data(role=m._chi12_role) is None
    assert m._model.item(2, 0).data(role=m._chi13_role) is None
    assert m._model.item(2, 0).data(role=m._chi23_role) is None

    # test asModel
    assert m._model == m.asModel()

