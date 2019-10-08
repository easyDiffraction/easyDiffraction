import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.CellParametersModel as Model

TEST_FILE = "file:Tests/Data/main.rcif"

def test_CellParametersModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.CellParametersModel(calculator)

    assert m._a_role == 257
    assert m._gamma_role == 262

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, dict)

    assert len(m._model.roleNames()) == 6

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 1
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=m._a_role) == 8.57
    assert m._model.item(0, 0).data(role=m._b_role) == 8.57
    assert m._model.item(0, 0).data(role=m._c_role) == 8.57
    assert m._model.item(0, 0).data(role=m._alpha_role) == 90.0
    assert m._model.item(0, 0).data(role=m._beta_role) == 90.0
    assert m._model.item(0, 0).data(role=m._gamma_role) == 90.0

    # test asModel
    assert m._model == m.asModel()


def test_CellParametersModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.CellParametersModel(calculator)

    # empty file
    file_path = QUrl("file:Tests/Data/Empty.rcif").toLocalFile()
    with pytest.raises(IndexError):
        calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    with pytest.raises(AttributeError):
        calculator = CryspyCalculator(file_path)
