import pytest

from PySide2.QtCore import Qt, QUrl, QModelIndex
from PySide2.QtGui import QStandardItemModel

from easyInterface.Diffraction.Calculators.CryspyCalculator import CryspyCalculator

from PyImports.QtInterface import QtCalculatorInterface
import PyImports.DisplayModels.FitablesModel as Model

TEST_FILE = "file:Tests/Data/main.cif"

def no_test_FitablesModelModel():

    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)


    assert isinstance(m._model, QStandardItemModel)

    # assure _setModelFromProject got called
    assert m._model.rowCount() == 22
    assert m._model.columnCount() == 1

    assert len(m._model.roleNames()) == len(m._roles_dict)
    assert b'path' in m._roles_dict.values()
    assert b'refine' in m._roles_dict.values()

    fr = Qt.UserRole + 1
    # Test stuff from _setModelFromProject here
    # first and last row
    assert m._model.item(0, 0).data(role=fr+1) == 'phases Fe3O4 cell length_a'
    assert m._model.item(0, 0).data(role=fr+2) == 8.36212
    assert m._model.item(0, 0).data(role=fr+3) == 0.0
    assert m._model.item(0, 0).data(role=fr+4) == pytest.approx(6.68969)
    assert m._model.item(0, 0).data(role=fr+5) == 10.034544
    assert m._model.item(0, 0).data(role=fr+6) is True
    assert m._model.item(0, 0).data(role=fr+7) == 'ang'

    assert m._model.item(21, 0).data(role=fr+1) == 'experiments pd resolution y'
    assert m._model.item(21, 0).data(role=fr+2) == 0.0
    assert m._model.item(21, 0).data(role=fr+3) == 0.0
    assert m._model.item(21, 0).data(role=fr+4) == 0.0
    assert m._model.item(21, 0).data(role=fr+5) == 0.0
    assert m._model.item(21, 0).data(role=fr+6) is False
    assert m._model.item(21, 0).data(role=fr+7) == ''

    # test asModel
    assert m._model == m.asModel()


def test_onModelChanged():
    file_path = QUrl(TEST_FILE).toLocalFile()
    calculator = CryspyCalculator(file_path)
    interface = QtCalculatorInterface(calculator)

    m = Model()
    m.setCalculatorInterface(interface)
    phase_index = m._model.index(2, 0)
    experiment_index = m._model.index(m._model.rowCount()-1, 0)

    # ######################
    # Check refine parameter
    # ######################

    display_role = Qt.UserRole + 7
    edit_role = Qt.UserRole + 107
    old_display = False
    old_edit = None
    new_display = True
    new_edit = True

    # Initial state
    assert m._model.data(phase_index, display_role) == old_display
    assert m._model.data(phase_index, edit_role) == old_edit
    assert m._model.data(experiment_index, display_role) == old_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via display role
    m._model.setData(phase_index, new_display, display_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == old_edit
    m._model.setData(experiment_index, new_display, display_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via edit role
    m._model.setData(phase_index, new_edit, edit_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == new_edit
    m._model.setData(experiment_index, new_edit, edit_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == new_edit

    # Edit value = display value
    m._model.setData(phase_index, new_edit, edit_role)
    assert m._model.data(phase_index, display_role) == new_display

    # #####################
    # Check value parameter
    # #####################

    display_role = Qt.UserRole + 3
    edit_role = Qt.UserRole + 103
    old_display = 0
    old_edit = None
    new_display = 0.5
    new_edit = 0.5

    # Initial state
    assert m._model.data(phase_index, display_role) == old_display
    assert m._model.data(phase_index, edit_role) == old_edit
    assert m._model.data(experiment_index, display_role) == old_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via display role
    m._model.setData(phase_index, new_display, display_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == old_edit
    m._model.setData(experiment_index, new_display, display_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via edit role
    m._model.setData(phase_index, new_edit, edit_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == new_edit
    m._model.setData(experiment_index, new_edit, edit_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == new_edit

    # ###################
    # Check min parameter
    # ###################

    display_role = Qt.UserRole + 5
    edit_role = Qt.UserRole + 105
    old_display = -1
    old_edit = None
    new_display = 0.5
    new_edit = 0.5

    # Initial state
    assert m._model.data(phase_index, display_role) == old_display
    assert m._model.data(phase_index, edit_role) == old_edit
    assert m._model.data(experiment_index, display_role) == old_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via display role
    m._model.setData(phase_index, new_display, display_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == old_edit
    m._model.setData(experiment_index, new_display, display_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via edit role
    m._model.setData(phase_index, new_edit, edit_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == new_edit
    m._model.setData(experiment_index, new_edit, edit_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == new_edit

    # ###################
    # Check max parameter
    # ###################

    display_role = Qt.UserRole + 6
    edit_role = Qt.UserRole + 106
    old_display = 1
    old_edit = None
    new_display = 0.5
    new_edit = 0.5

    # Initial state
    assert m._model.data(phase_index, display_role) == old_display
    assert m._model.data(phase_index, edit_role) == old_edit
    assert m._model.data(experiment_index, display_role) == old_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via display role
    m._model.setData(phase_index, new_display, display_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == old_edit
    m._model.setData(experiment_index, new_display, display_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == old_edit

    # Model changes via edit role
    m._model.setData(phase_index, new_edit, edit_role)
    assert m._model.data(phase_index, display_role) == new_display
    assert m._model.data(phase_index, edit_role) == new_edit
    m._model.setData(experiment_index, new_edit, edit_role)
    assert m._model.data(experiment_index, display_role) == new_display
    assert m._model.data(experiment_index, edit_role) == new_edit
