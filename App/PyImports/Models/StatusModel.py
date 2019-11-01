from functools import reduce

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers
import collections

class StatusList(collections.MutableSet):
    def __init__(self, list=None):
        if list is None:
            self._store = []
        else:
            self._store = list

    def __contains__(self, item):
        return item in self._store

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def add(self, item):
        if item not in self._store:
            self._store.append(item)

    def discard(self, item):
        try:
            self._store.remove(item)
        except ValueError:
            pass

    def getItem(self, itemName):
        for item in self._store:
            if item.name == itemName:
                return item
        return None

    def setItemValue(self, itemName, value):
        item = self.getItem(itemName)
        if item is None:
            raise KeyError
        item.value = value

    def getItemValue(self, itemName, previous=False):
        item = self.getItem(itemName)
        if item is None:
            raise KeyError
        return item.value

    def getItems(self):
        return self._store


class StatusItem():
    def __init__(self, name, value=None, title=None):
        self._name = name
        self._value = value
        self._previous = None
        self._title = title
        self._previousTitle = None
        self._returnPrevious = False
    @property
    def name(self):
        if self._returnPrevious & self.hasPrevious:
            return self._name + '_previous'
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def value(self):
        if self._returnPrevious & self.hasPrevious:
            if self._previous == self._value:
                return None
            return self._previous
        return self._value

    @value.setter
    def value(self, value):
        self._previous = self._value
        self._value = value

    @property
    def previous(self):
        return self._previous

    @property
    def title(self):
        if self._returnPrevious & self.hasPrevious:
            return self._previousTitle
        if self._title is None:
            return self._name
        return self._title

    @title.setter
    def title(self, value):
        if self._returnPrevious:
            self._previousTitle = value
        else:
            self._title = value

    @property
    def hasPrevious(self):
        if self._previousTitle is None:
            return False
        else:
            return True

    def setReturn(self, value):
        self._returnPrevious = value

    def copy(self):
        return StatusItem(self._name, self._value, self._title)

class StatusModel(QObject):
    def __init__(self, calculator, parent=None):
        super().__init__(parent)

        # major properties
        self._calculator = calculator

        chiItem = StatusItem('chiSq', title='Goodnes-of-fit (\u03c7\u00b2)')
        chiItem.setReturn(True)
        chiItem.title = 'Previous goodnes-of-fit (\u03c7\u00b2)'
        chiItem.setReturn(False)
        self._interestedList = StatusList([
            chiItem,
            StatusItem('numPars', title='Number of parameters'),
            StatusItem('numPhases', title='Number of phases'),
            StatusItem('numData', title='Number of data files')
        ])
        self._updateStatusList()

        # minor properties
        self._first_role = Qt.UserRole + 1

        self._model = QStandardItemModel()
        # set role names
        self._role_names_list= ['label', 'value']
        self._roles_list = []
        self._roles_dict = {}
        self._setRolesListAndDict()
        self._model.setItemRoleNames(self._roles_dict)
        # set model
        self._setModelFromProject() # !!!!!!!!
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
        column = []

        self._updateStatusList()

        def makeItem(thisInterest):
            item = QStandardItem()
            for role, role_name_bytes in self._roles_dict.items():
                role_name = role_name_bytes.decode()
                if role_name == 'label':
                    value = thisInterest.title
                elif role_name == 'value':
                    value = thisInterest.value
                else:
                    continue
                item.setData(value, role)
            return item

        for interest in self._interestedList:
            column.append(makeItem(interest))
            if interest.hasPrevious:
                interest.setReturn(True)
                if interest.value is not None:
                    column.append(makeItem(interest))
                interest.setReturn(False)

        # set model
        self._model.appendColumn(column) # dataChanged is not emited. why?

        #TODO check why
        self._model.dataChanged.emit(self._model.index(0, 0), self._model.index(self._model.rowCount()-1, self._model.columnCount()-1), self._roles_list)


    def _updateStatusList(self):
        project_dict = self._calculator.asDict()

        # Set chi squared
        self._interestedList.setItemValue('chiSq', round(project_dict['info']['chi_squared']['value'], 2))

        # Set number of parameters
        numPars = 0
        for path in Helpers.find_in_obj(project_dict, 'refine'):
            keys_list = path[:-1]
            hide = Helpers.nested_get(project_dict, keys_list + ['hide'])
            if hide:
                continue
            if Helpers.nested_get(project_dict, keys_list + ['refine']):
                numPars = numPars+1

        self._interestedList.setItemValue('numPars', numPars)
        self._interestedList.setItemValue('numPhases', len(project_dict['phases']))
        self._interestedList.setItemValue('numData', len(project_dict['experiments']))

    modelChanged = Signal()

    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()
        self.modelChanged.emit()

    def asModel(self):
        """Return model."""
        return self._model
