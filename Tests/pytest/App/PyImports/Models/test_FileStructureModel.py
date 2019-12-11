import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.Models.FileStructureModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_FileStructureModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.FileStructureModel()
    m.setCalculator(calculator)

    assert isinstance(m._data_model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._data_model.rowCount() == 2
    assert m._data_model.columnCount() == 1

    role_1 = Qt.UserRole + 1
    role_2 = Qt.UserRole + 2

    assert len(m._data_model.roleNames()) == 2
    assert m._data_model.roleNames()[role_1] == b"phasesRole"
    assert str(m._data_model.roleNames()[role_2]) == "b'experimentsRole'"

    assert 'data_Fe3O4' in m._data_model.item(0, 0).data(role=role_1)
    assert 'data_pnd' in m._data_model.item(1, 0).data(role=role_2)



