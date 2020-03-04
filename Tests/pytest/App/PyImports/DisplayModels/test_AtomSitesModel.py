import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from PyImports.QtInterface import QtCalculatorInterface, ProjectDict

import PyImports.DisplayModels.AtomSitesModel as Model

TEST_FILE = "file:Tests/Data/main.cif"


def test_AtomSitesModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    assert m._label_role == 257
    assert m._occupancy_role == 263

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 3
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data() == 'Fe3A'
    assert m._model.item(0, 0).data(role=m._atom_role) == 'Fe3+'
    assert m._model.item(0, 0).data(role=m._color_role) == 0.945
    assert m._model.item(0, 0).data(role=m._x_role) == 0.125
    assert m._model.item(0, 0).data(role=m._y_role) == 0.125
    assert m._model.item(0, 0).data(role=m._z_role) == 0.125
    assert m._model.item(0, 0).data(role=m._occupancy_role) == 1.0

    assert m._model.item(1, 0).data() == 'Fe3B'
    assert m._model.item(1, 0).data(role=m._atom_role) == 'Fe3+'
    assert m._model.item(1, 0).data(role=m._color_role) == 0.945
    assert m._model.item(1, 0).data(role=m._x_role) == 0.5
    assert m._model.item(1, 0).data(role=m._y_role) == 0.5
    assert m._model.item(1, 0).data(role=m._z_role) == 0.5
    assert m._model.item(1, 0).data(role=m._occupancy_role) == 1.0

    assert m._model.item(2, 0).data() == 'O'
    assert m._model.item(2, 0).data(role=m._atom_role) == 'O2-'
    assert m._model.item(2, 0).data(role=m._color_role) == 0.5803
    assert m._model.item(2, 0).data(role=m._x_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._y_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._z_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._occupancy_role) == 1.0

    # test asModel
    assert m._model == m.asModel()

