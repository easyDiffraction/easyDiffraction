from functools import reduce

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers

class StatusModel(QObject):
    def __init__(self, calculator, parent=None):
        super().__init__(parent)

        self._interestedDict = {
            'current': {
                'chiSq': None,
                'numPars': None,
                'numPhases': None,
                'numData': None
            },
            'previous': None
        }

        self._first_role = Qt.UserRole + 1
        # self._edit_role_increment = 100
        # self._edit_role_name_suffix = 'Edit'

        self._model = QStandardItemModel()
        # set role names
        self._role_names_list= ['label', 'value']
        self._roles_list = []
        self._roles_dict = {}
        self._setRolesListAndDict()
        self._model.setItemRoleNames(self._roles_dict)

        self._calculator = calculator

        # connect signals
        self._calculator.projectDictChanged.connect(self.onProjectChanged)

    def _setRolesListAndDict(self):
        """..."""
        for i, role_name in enumerate(self._role_names_list):
            display_role = self._first_role + i
            # edit_role = display_role + self._edit_role_increment
            self._roles_dict[display_role] = role_name.encode()
            # self._roles_dict[edit_role] = '{}{}'.format(role_name, self._edit_role_name_suffix).encode()
            self._roles_list.append(display_role)
            # self._roles_list.append(edit_role)


    def _setModelFromProject(self):
        """Create the initial data list with structure for GUI fitables table."""
        self._model.setColumnCount(0) # faster than clear(); clear() crashes app! why?
        self._makeMyDict()
        column = []

        for interest in self._interestedDict['current'].items():
            item = QStandardItem()
            for role, role_name_bytes in self._roles_dict.items():
                role_name = role_name_bytes.decode()
                if role_name == 'label':
                    value = interest[0]
                elif role_name == 'value':
                    value = interest[1]
                else:
                    continue
                item.setData(value, role)
            column.append(item)
            
        # set model
        self._model.appendColumn(column) # dataChanged is not emited. why?

        #TODO check why
        self._model.dataChanged.emit(self._model.index(0, 0), self._model.index(self._model.rowCount()-1, self._model.columnCount()-1), self._roles_list)


    def _makeMyDict(self):
        project_dict = self._calculator.asDict()
        self._interestedDict['previous'] = self._interestedDict['current'].copy()
        # Set chi squared
        self._interestedDict['current']['chiSq'] = project_dict['info']['chi_squared']['value']
        # Set number of parameters
        numPars = 0
        for path in Helpers.find_in_obj(project_dict, 'refine'):
            keys_list = path[:-1]
            hide = Helpers.nested_get(project_dict, keys_list + ['hide'])
            if hide:
                continue
            item = QStandardItem()
            for role, role_name_bytes in self._roles_dict.items():
                role_name = role_name_bytes.decode()
                if role_name == 'refine':
                    if Helpers.nested_get(project_dict, keys_list + [role_name]) == 1:
                         numPars = numPars + 1
        self._interestedDict['current']['numPars'] = numPars

    modelChanged = Signal()

    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()
        self.modelChanged.emit()

    def asModel(self):
        """Return model."""
        return self._model