import logging

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel

from easyInterface.Utils.Helpers import find_in_obj, nested_get
from PyImports.DisplayModels.BaseModel import BaseModel


class FitablesModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # minor properties
        self._first_role = Qt.UserRole + 1
        self._edit_role_increment = 100
        self._edit_role_name_suffix = 'Edit'
        # major properties
        self._calculator = None
        self._model = QStandardItemModel()
        # set role names
        self._role_names_list = ['path', 'label', 'value', 'error', 'min', 'max', 'refine', 'unit']
        self._roles_list = []
        self._roles_dict = {}
        self._setRolesListAndDict()
        self._model.setItemRoleNames(self._roles_dict)
        # connect signals
        self._model.dataChanged.connect(self.onModelChanged)

    def _setRolesListAndDict(self):
        """..."""
        for i, role_name in enumerate(self._role_names_list):
            display_role = self._first_role + i
            edit_role = display_role + self._edit_role_increment
            self._roles_dict[display_role] = role_name.encode()
            self._roles_dict[edit_role] = '{}{}'.format(role_name, self._edit_role_name_suffix).encode()
            self._roles_list.append(display_role)
            self._roles_list.append(edit_role)

    def _setModelsFromProjectDict(self):
        """Create the initial data list with structure for GUI fitables table."""
        # block model signals
        self._model.blockSignals(True)
        # reset model
        self._model.setColumnCount(0) # faster than clear(); clear() crashes app! why?
        project_dict = self._project_dict
        # set column
        column = []
        for path in find_in_obj(project_dict.asDict(), 'refine'):
            keys_list = path[:-1]
            hide = project_dict.getItemByPath(keys_list + ['hide'])
            if hide:
                continue
            item = QStandardItem()
            for role, role_name_bytes in self._roles_dict.items():
                role_name = role_name_bytes.decode()
                if role_name.endswith(self._edit_role_name_suffix):
                    continue
                if role_name == 'path':
                    value = keys_list
                elif role_name == 'label':
                    value = ' '.join(keys_list[:-1])
                elif role_name == 'value':
                    value = project_dict.getItemByPath(keys_list[:-1]).value
                elif role_name == 'min':
                    value = project_dict.getItemByPath(keys_list).min
                elif role_name == 'max':
                    value = project_dict.getItemByPath(keys_list).max
                elif role_name == 'unit':
                    value = str(nested_get(project_dict, keys_list + [role_name])) # conversion to str is needed if role = unit !
                else:
                    value = nested_get(project_dict, keys_list + [role_name])
                item.setData(value, role)
            column.append(item)
        # set model
        self._model.appendColumn(column) # dataChanged is not emited. why?
        # unblock signals and emit model layout changed
        self._model.blockSignals(False)
        self._model.layoutChanged.emit()
        # Emit signal which is catched by the QStandartItemModel-based
        # QML GUI elements in order to update their views

    def _updateProjectByIndexAndRole(self, index, edit_role):
        """Update project element, which is changed in the model, depends on its index and role."""
        display_role = edit_role - self._edit_role_increment
        display_role_name = self._roles_dict[display_role].decode()
        path_role = self._role_names_list.index('path') + self._first_role
        keys_list = self._model.data(index, path_role) + [display_role_name]
        edit_value = self._model.data(index, edit_role)
        display_value = self._model.data(index, display_role)

        fitable_name = '.'.join(keys_list[:-3])
        fitable_value = edit_value
        undo_redo_text = f"Changing '{fitable_name}' to '{fitable_value:.4f}'"
        self._calculator_interface.project_dict.startBulkUpdate(undo_redo_text)
        self._calculator_interface.canUndoOrRedoChanged.emit()

        if edit_value != display_value:
            if isinstance(edit_value, bool):
                if 'phases' == keys_list[0]:
                    self._calculator_interface.setPhaseRefine(keys_list[1], keys_list[2:-2], edit_value)
                elif 'experiments' == keys_list[0]:
                    self._calculator_interface.setExperimentRefine(keys_list[1], keys_list[2:-2], edit_value)
                else:
                    self._calculator_interface.setDictByPath(keys_list, edit_value)
            else:
                if 'phases' == keys_list[0]:
                    self._calculator_interface.setPhaseValue(keys_list[1], keys_list[2:-2], edit_value)
                    self._calculator_interface.updateCalculations()
                elif 'experiments' == keys_list[0]:
                    self._calculator_interface.setExperimentValue(keys_list[1], keys_list[2:-2], edit_value)
                    self._calculator_interface.updateCalculations()
                else:
                    self._calculator_interface.setDictByPath(keys_list, edit_value)

        self._calculator_interface.project_dict.endBulkUpdate()
        self._calculator_interface.canUndoOrRedoChanged.emit()

    def onModelChanged(self, top_left_index, bottom_right_index, roles):
        """Define what to do if model is changed, e.g. from GUI."""
        role = roles[0]
        role_name = self._roles_dict[role].decode()
        if role_name.endswith(self._edit_role_name_suffix):
            index = top_left_index
            edit_role = role
            self._updateProjectByIndexAndRole(index, edit_role)
