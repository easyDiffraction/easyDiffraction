import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.Interface import ProjectDict

from PyImports.QtInterface import QtCalculatorInterface
import PyImports.DisplayModels.CellParametersModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_CellParametersModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)



    assert m._a_role == 257
    assert m._gamma_role == 262

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    assert len(m._model.roleNames()) == 6

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 1
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=m._a_role) == 8.36212
    assert m._model.item(0, 0).data(role=m._b_role) == 8.36212
    assert m._model.item(0, 0).data(role=m._c_role) == 8.36212
    assert m._model.item(0, 0).data(role=m._alpha_role) == 90.0
    assert m._model.item(0, 0).data(role=m._beta_role) == 90.0
    assert m._model.item(0, 0).data(role=m._gamma_role) == 90.0

    # test asModel
    assert m._model == m.asModel()
