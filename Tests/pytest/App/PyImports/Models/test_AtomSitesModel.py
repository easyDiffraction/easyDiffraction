import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from EasyInterface.Calculators.CryspyCalculator import CryspyCalculator
from EasyInterface.Interface import CalculatorInterface

import PyImports.DisplayModels.AtomSitesModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_AtomSitesModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = CalculatorInterface(calculator)

    m = Model.AtomSitesModel()
    m.setCalculatorInterface(interface)

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

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

    assert m._model.item(2, 0).data() == 'O1'
    assert m._model.item(2, 0).data(role=m._atom_role) == 'O2-'
    assert m._model.item(2, 0).data(role=m._color_role) == 0.5803
    assert m._model.item(2, 0).data(role=m._x_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._y_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._z_role) == 0.25521
    assert m._model.item(2, 0).data(role=m._occupancy_role) == 1.0

    # test asModel
    assert m._model == m.asModel()


def test_AtomSitesModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.AtomSitesModel()
        m.setCalculatorInterface(calculator)

    # empty file
    #file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    #with pytest.raises(IndexError):
    #    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
