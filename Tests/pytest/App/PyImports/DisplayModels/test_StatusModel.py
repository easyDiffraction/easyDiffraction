import pytest

from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator
from easyInterface.Diffraction.QtInterface import QtCalculatorInterface,  ProjectDict

import PyImports.DisplayModels.StatusModel as Model

TEST_FILE = "file:Tests/Data/main.cif"


def test_StatusModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)


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
    assert m._statusBarModel.item(0, 0).data(role=fr + 1) == pytest.approx(340.79)
    assert m._statusBarModel.item(2, 0).data(role=fr + 1) == 1
    assert m._statusBarModel.item(3, 0).data(role=fr + 1) == 1
    assert m._statusBarModel.item(1, 0).data(role=fr + 1) == 1

    assert m._chartDisplayModel.item(0, 0).data(role=fr + offset + 1) == pytest.approx(340.79)
    assert m._chartDisplayModel.item(1, 0).data(role=fr + offset + 1) == 1

    assert m._statusBarModel == m.returnStatusBarModel()
    assert m._chartDisplayModel == m.returnChartModel()


