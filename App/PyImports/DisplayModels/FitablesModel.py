import numpy as np

from easyInterface import logger

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel

from easyInterface.Utils.Helpers import find_in_obj, nested_get
from PyImports.DisplayModels.BaseModel import BaseModel


class FitablesModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._log = logger.getLogger(self.__class__.__module__)
        # limits
        self._left_limit_for_zero_value = -1
        self._right_limit_for_zero_value = 1
        self._limit_percentage_deviation = 0.2
        # minor properties
        self._first_role = Qt.UserRole + 1
        self._edit_role_increment = 100
        self._edit_role_name_suffix = 'Edit'
        # major properties
        self._model = QStandardItemModel()
        # set role names
        self._role_names_list = ['path', 'label', 'value', 'error', 'min', 'max', 'refine', 'unit',
                                 'labelList']  # 257 - 265
        self._roles_list = []
        self._roles_dict = {}
        self._setRolesListAndDict()
        self._model.setItemRoleNames(self._roles_dict)
        # connect signals
        self._model.dataChanged.connect(self.onModelChanged)

    def _setRolesListAndDict(self):
        """
        Create the display and edit role list and dict from role names.
        """
        for i, role_name in enumerate(self._role_names_list):
            display_role = self._first_role + i
            edit_role = display_role + self._edit_role_increment

            self._roles_dict[display_role] = role_name.encode()
            self._roles_dict[edit_role] = '{}{}'.format(role_name, self._edit_role_name_suffix).encode()
            self._roles_list.append(display_role)
            self._roles_list.append(edit_role)

        self._log.debug(f"roles: {self._roles_dict}")

    def _setModelsFromProjectDict(self):
        """
        Create the initial data list with structure for GUI fitables table.
        """
        self._log.info("Starting to set Model from Project Dict")

        # block model signals
        self._model.blockSignals(True)

        # reset model
        self._model.setColumnCount(0)  # faster than clear(); clear() crashes app! why?
        self._model.setRowCount(0)

        # sort background
        for experiment in self._project_dict['experiments'].keys():
            self._project_dict['experiments'][experiment]['background'].sort()

        # set column
        column = []
        for path in find_in_obj(self._project_dict.asDict(), 'refine'):
            keys_list = path[:-1]
            hide = self._project_dict.getItemByPath(keys_list + ['hide'])
            if hide:
                continue

            item = QStandardItem()
            for role, role_name_bytes in self._roles_dict.items():
                role_name = role_name_bytes.decode()
                if role_name.endswith(self._edit_role_name_suffix):
                    continue
                if role_name == 'path':
                    value = keys_list
                elif role_name == 'labelList':
                    value = keys_list[0:-1]
                    # Insert elements according to CIF
                    if len(value) > 0 and value[-1] == "offset": value.insert(-1, "setup")
                    if len(value) > 0 and value[-1] == "wavelength": value.insert(-1, "setup")
                    # Renaming according to CIF
                    if len(value) > 0 and value[-1] == "offset": value[-1] = "offset_2theta"
                    if len(value) > 2 and value[2] == "atoms": value[2] = "atom_site"
                    if len(value) > 2 and value[2] == "resolution": value[2] = "pd_instr_resolution"
                    if len(value) > 2 and value[2] == "polarization": value[2] = "diffrn_radiation"
                    if len(value) > 2 and value[2] == "background": value.insert(3, "2theta")
                    if len(value) > 5 and value[4] == "MSP":
                        value[5] = "susceptibility_" + value[5]
                        del value[4]
                elif role_name == 'label':
                    value = ' '.join(keys_list[:-1])
                elif role_name == 'value':
                    value = self._project_dict.getItemByPath(keys_list[:-1]).value
                elif role_name == 'min':
                    value = self._project_dict.getItemByPath(keys_list).min
                elif role_name == 'max':
                    value = self._project_dict.getItemByPath(keys_list).max
                elif role_name == 'unit':
                    # conversion to str is needed if role = unit !
                    value = str(nested_get(self._project_dict, keys_list + [role_name]))
                else:
                    value = nested_get(self._project_dict, keys_list + [role_name])
                item.setData(value, role)

            column.append(item)

        # set model
        self._model.appendColumn(column)  # dataChanged is not emited. why?

        # unblock signals and emit model layout changed
        self._model.blockSignals(False)
        self._model.layoutChanged.emit()
        self._log.info("Finished setting Model from Project Dict")
        # Emit signal which is caught by the QStandardItemModel-based
        # QML GUI elements in order to update their views

    def _updateProjectByIndexAndRole(self, index, edit_role):
        """
        Update project element, which is changed in the model, depends on its index and role.
        """
        self._log.info("Starting updating Project Dict from Model")

        display_role = edit_role - self._edit_role_increment
        display_role_name = self._roles_dict[display_role].decode()
        path_role = self._role_names_list.index('path') + self._first_role
        keys_list = self._model.data(index, path_role) + [display_role_name]
        edit_value = self._model.data(index, edit_role)
        display_value = self._model.data(index, display_role)
        self._log.debug(f"edit_role: {edit_role}")
        self._log.debug(f"display_role: {display_role}")
        self._log.debug(f"display_role_name: {display_role_name}")
        self._log.debug(f"path_role: {path_role}")
        self._log.debug(f"keys_list: {keys_list}")
        self._log.debug(f"edit_value: {edit_value}")
        self._log.debug(f"display_value: {display_value}")

        fitable_name = '.'.join(keys_list[:-2])
        fitable_value = edit_value
        data_block_name = keys_list[0]
        self._log.debug(f"fitable_name: {fitable_name}")
        self._log.debug(f"fitable_value: {fitable_value}")
        self._log.debug(f"data_block_name: {data_block_name}")

        if display_role_name == 'refine':
            undo_redo_text = f"Changing '{fitable_name}' refine state to '{fitable_value}'"
            self._log.debug(f"undo_redo_text: {undo_redo_text}")
            self._calculator_interface.project_dict.startBulkUpdate(undo_redo_text)
            self._calculator_interface.canUndoOrRedoChanged.emit()
            if data_block_name == 'phases':
                try:
                    self._calculator_interface.setPhaseRefine(keys_list[1], keys_list[2:-2], edit_value)
                except AttributeError:
                    # In this case the calculator/dict are out of phase :-/ So fallback to manual.
                    self._calculator_interface.project_dict.setItemByPath(keys_list, edit_value)
                # self._calculator_interface.updatePhases()
            elif data_block_name == 'experiments':
                try:
                    self._calculator_interface.setExperimentRefine(keys_list[1], keys_list[2:-2], edit_value)
                except AttributeError:
                    self._calculator_interface.project_dict.setItemByPath(keys_list, edit_value)
                # self._calculator_interface.updateExperiments()
            else:
                self._calculator_interface.setDictByPath(keys_list, edit_value)
            self._calculator_interface.projectDictChanged.emit()

        elif display_role_name == 'value':
            undo_redo_text = f"Changing '{fitable_name}' to '{fitable_value:.4f}'"
            self._log.debug(f"undo_redo_text: {undo_redo_text}")
            self._calculator_interface.project_dict.startBulkUpdate(undo_redo_text)
            self._calculator_interface.canUndoOrRedoChanged.emit()
            if data_block_name == 'phases':
                try:
                    self._calculator_interface.setPhaseValue(keys_list[1], keys_list[2:-2], edit_value)
                except AttributeError:
                    self._calculator_interface.project_dict.setItemByPath(keys_list, edit_value)
                    self._calculator_interface.updatePhases()
                self._calculator_interface.updateCalculations()  # phases also updated ?
            elif data_block_name == 'experiments':
                try:
                    self._calculator_interface.setExperimentValue(keys_list[1], keys_list[2:-2], edit_value)
                except AttributeError:
                    self._calculator_interface.project_dict.setItemByPath(keys_list, edit_value)
                    self._calculator_interface.updateExperiments()
                self._calculator_interface.updateCalculations()  # experiments also updated ?
            else:
                self._calculator_interface.setDictByPath(keys_list, edit_value)
            # Update min and max if value is outside [min, max] range
            value = self._calculator_interface.project_dict.getItemByPath(keys_list)
            min_value = self._calculator_interface.project_dict.getItemByPath([*keys_list[:-1], 'min'])
            max_value = self._calculator_interface.project_dict.getItemByPath([*keys_list[:-1], 'max'])
            self._log.debug(f"initial min: {min}, max: {max}")
            # TODO: the code below duplicates the code from BaseClasses.py - class Base - def updateMinMax
            # stacked changes (for GUI triggered changes)
            if np.isclose([value], [0]):
                min_value = self._left_limit_for_zero_value
                max_value = self._right_limit_for_zero_value
            if value < min_value:
                if value > 0:
                    min_value = value * (1 - self._limit_percentage_deviation)
                else:
                    min_value = value * (1 + self._limit_percentage_deviation)
            if value > max_value:
                if value > 0:
                    max_value = value * (1 + self._limit_percentage_deviation)
                else:
                    max_value = value * (1 - self._limit_percentage_deviation)
            # Update min and max in project dict
            self._log.debug(f"re-calculated min: {min}, max: {max}")
            self._calculator_interface.project_dict.setItemByPath([*keys_list[:-1], 'min'], min_value)
            self._calculator_interface.project_dict.setItemByPath([*keys_list[:-1], 'max'], max_value)
            self._calculator_interface.projectDictChanged.emit()

        elif display_role_name == 'min' or display_role_name == 'max':
            undo_redo_text = f"Changing '{fitable_name}' {display_role_name} to '{fitable_value}'"
            self._log.debug(f"undo_redo_text: {undo_redo_text}")
            self._calculator_interface.project_dict.startBulkUpdate(undo_redo_text)
            self._calculator_interface.canUndoOrRedoChanged.emit()
            # TODO: try to use setDictByPath below
            # self._calculator_interface.setDictByPath(keys_list, edit_value)
            # Temporary (?) solution until above is fixed
            self._calculator_interface.project_dict.setItemByPath(keys_list, edit_value)
            self._calculator_interface.projectDictChanged.emit()

        else:
            self._log.warning(f"unsupported role: {display_role_name}")
            return

        self._calculator_interface.project_dict.endBulkUpdate()
        self._calculator_interface.canUndoOrRedoChanged.emit()
        self._log.info("Finished updating Project Dict from Model")


    def onModelChanged(self, top_left_index, bottom_right_index, roles):
        """
        Define what to do if model is changed, e.g. from GUI.
        """
        role = roles[0]
        role_name = self._roles_dict[role].decode()
        self._log.debug(f"roles: {roles}")
        self._log.debug(f"role: {role}")
        self._log.debug(f"role_name: {role_name}")

        if role_name.endswith(self._edit_role_name_suffix):
            self._updateProjectByIndexAndRole(top_left_index, role)
