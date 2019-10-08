import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.CellBoxModel as Model

TEST_FILE = "file:Tests/Data/main.rcif"

def test_CellBoxModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.CellBoxModel(calculator)

    assert m._x_role == 257
    assert m._y_role == 258
    assert m._z_role == 259

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    assert len(m._model.roleNames()) == 3

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 3084
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=m._x_role) == 0.0
    assert m._model.item(0, 0).data(role=m._y_role) == 0.0
    assert m._model.item(0, 0).data(role=m._z_role) == 0.0

    assert m._model.item(3083, 0).data(role=m._x_role) == 8.57
    assert m._model.item(3083, 0).data(role=m._y_role) == 8.57
    assert m._model.item(3083, 0).data(role=m._z_role) == 8.536653696498055

    # test asModel
    assert m._model == m.asModel()


def test_CellBoxModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.CellBoxModel(calculator)

    # empty file
    file_path = QUrl("file:Tests/Data/Empty.rcif").toLocalFile()
    with pytest.raises(IndexError):
        calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
