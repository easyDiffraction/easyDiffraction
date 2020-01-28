import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from PyImports.Calculators.CryspyCalculator import CryspyCalculator

import PyImports.DisplayModels.StatusModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def test_StatusModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)

    m = Model.StatusModel()
    m.setCalculatorInterface(calculator)


    assert isinstance(m._statusBarModel, QStandardItemModel)
    assert isinstance(m._chartDisplayModel, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._statusBarModel.rowCount() == 4
    assert m._statusBarModel.columnCount() == 1

    assert m._chartDisplayModel.rowCount() == 2
    assert m._chartDisplayModel.columnCount() == 1

    assert len(m._statusBarModel.roleNames()) == len(m._roles_dict['status'])
    assert len(m._chartDisplayModel.roleNames()) == len(m._roles_dict['plot'])

    assert b'label' in m._roles_dict['status'].values()
    assert b'value' in m._roles_dict['status'].values()

    assert b'label' in m._roles_dict['plot'].values()
    assert b'value' in m._roles_dict['plot'].values()

    fr = Qt.UserRole + 1
    offset = 100
    assert m._statusBarModel.item(0, 0).data(role=fr + 1) == pytest.approx(71.95)
    assert m._statusBarModel.item(2, 0).data(role=fr + 1) == 1
    assert m._statusBarModel.item(3, 0).data(role=fr + 1) == 1
    assert m._statusBarModel.item(1, 0).data(role=fr + 1) == 5

    assert m._chartDisplayModel.item(0, 0).data(role=fr + offset + 1) == pytest.approx(71.95)
    assert m._chartDisplayModel.item(1, 0).data(role=fr + offset + 1) == 5

    assert m._statusBarModel == m.returnStatusBarModel()
    assert m._chartDisplayModel == m.returnChartModel()


def test_StatusModelModel_bad_calculator():

    calculator = None

    # null calculator
    with pytest.raises(AttributeError):
        m = Model.StatusModel()
        m.setCalculatorInterface(calculator)

