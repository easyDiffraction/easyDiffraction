import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Interface import CalculatorInterface

import PyImports.DisplayModels.FileStructureModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_FileStructureModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = CalculatorInterface(calculator)

    m = Model.FileStructureModel()
    m.setCalculatorInterface(interface)

    assert isinstance(m._model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 1
    assert m._model.columnCount() == 1

    phaseRole = Qt.UserRole + 1
    expRole = Qt.UserRole + 2
    calcRole = Qt.UserRole + 3

    assert len(m._model.roleNames()) == 3
    assert m._model.roleNames()[phaseRole] == b"phasesRole"
    assert str(m._model.roleNames()[expRole]) == "b'experimentsRole'"
    assert str(m._model.roleNames()[calcRole]) == "b'calculationsRole'"

    assert 'data_Fe3O4' in m._model.item(0, 0).data(role=phaseRole)
    assert 'data_pd' in m._model.item(0, 0).data(role=expRole)
    assert '_refln_index_k' in m._model.item(0, 0).data(role=calcRole)
