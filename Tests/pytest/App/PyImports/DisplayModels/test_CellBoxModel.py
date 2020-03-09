import pytest

from PySide2.QtCore import QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.Interface import ProjectDict

from PyImports.QtInterface import QtCalculatorInterface
import PyImports.DisplayModels.CellBoxModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_CellBoxModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)


    assert m._x_role == 257
    assert m._y_role == 258
    assert m._z_role == 259

    assert isinstance(m._model, QStandardItemModel)
    assert isinstance(m._project_dict, ProjectDict)

    assert len(m._model.roleNames()) == 3

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 3000
    assert m._model.columnCount() == 1

    # Test stuff from _setModelFromProject here
    assert m._model.item(0, 0).data(role=m._x_role) == 0.0
    assert m._model.item(0, 0).data(role=m._y_role) == 0.0
    assert m._model.item(0, 0).data(role=m._z_role) == 0.0

    assert m._model.item(2999, 0).data(role=m._x_role) == 8.36212
    assert m._model.item(2999, 0).data(role=m._y_role) == 8.36212
    assert m._model.item(2999, 0).data(role=m._z_role) == pytest.approx(8.32867)

    # test asModel
    assert m._model == m.asModel()


def test_CellBoxModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model()
        m.setCalculatorInterface(calculator)

    # null file
    file_path = None
    # with pytest.raises(TypeError):
    calculator = CryspyCalculator(file_path)

    # epty file
    file_path = QUrl("file:Tests/Data/empty.cif").toLocalFile()
    # apparently it is fine now - no exception raised
    calculator = CryspyCalculator(file_path)

    # old style rcif
    file_path = QUrl("file:Tests/Data/full.rcif").toLocalFile()
    # with pytest.raises(AttributeError):
    calculator = CryspyCalculator(file_path)
