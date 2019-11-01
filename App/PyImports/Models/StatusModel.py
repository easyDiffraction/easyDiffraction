from functools import reduce

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers
import collections


class StatusList(collections.MutableSet):
    def __init__(self, itemList=None):
        if itemList is None:
            self._store = []
        else:
            self._store = itemList

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


class StatusItem:
    def __init__(self, name, value=None, title=None, additionalData=None):
        self._name = name
        self._value = value
        self._previous = None
        self._title = title
        self._previousTitle = None
        self._returnPrevious = False
        self.additionalData = additionalData

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
        if value == self._value:
            return
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

        # Create the status items
        chiItem = StatusItem('chiSq', title='Goodnes-of-fit (\u03c7\u00b2)', additionalData=1)
        chiItem.setReturn(True)
        chiItem.title = 'Previous goodnes-of-fit (\u03c7\u00b2)'
        chiItem.setReturn(False)
        self._interestedList = StatusList([
            chiItem,
            StatusItem('numPars', title='Number of parameters', additionalData=1),
            StatusItem('numPhases', title='Number of phases', additionalData=0),
            StatusItem('numData', title='Number of data files', additionalData=0)
        ])
        self._updateStatusList()

        # minor properties
        self._first_role = Qt.UserRole + 1

        self._statusBarModel = QStandardItemModel()
        self._chartDisplayModel = QStandardItemModel()
        # set role names
        self._role_names_list = ['label', 'value']
        self._roles_list = []
        self._roles_dict = {'status': {},
                            'plot': {}}
        self._setRolesListAndDict()
        self._statusBarModel.setItemRoleNames(self._roles_dict['status'])
        self._chartDisplayModel.setItemRoleNames(self._roles_dict['plot'])
        # set model
        self._setModelFromProject()
        # connect to project changed signals
        self._calculator.projectDictChanged.connect(self.onProjectChanged)

    def _setRolesListAndDict(self):
        """..."""
        offset = 100
        for i, role_name in enumerate(self._role_names_list):
            display_role = self._first_role + i
            self._roles_dict['status'][display_role] = role_name.encode()
            self._roles_list.append(display_role)
            self._roles_dict['plot'][self._first_role + i + offset] = role_name.encode()

    def _setModelFromProject(self):
        """Create the initial data list with structure for GUI fitables table."""
        self._statusBarModel.removeColumns(0, self._statusBarModel.columnCount())
        self._chartDisplayModel.removeColumns(0, self._chartDisplayModel.columnCount())

        columnStatusBar = []
        columnChartDisplay = []

        self._updateStatusList()

        def makeItem(thisInterest, offset=0):
            """Make an item. This can be a plot or status bar"""
            if offset == 1:
                theseItems = self._roles_dict['plot'].items()
            else:
                theseItems = self._roles_dict['status'].items()
            item = QStandardItem()
            for role, role_name_bytes in theseItems:
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
            # Add the status bar item
            columnStatusBar.append(makeItem(interest))
            # Does this need to added to the plot?
            if interest.additionalData == 1:
                columnChartDisplay.append(makeItem(interest, offset=1))

            # Does this item also have previous values which need to be shown?
            if interest.hasPrevious:
                interest.setReturn(True)
                if interest.value is not None:
                    columnStatusBar.append(makeItem(interest))
                interest.setReturn(False)

        # Set the models
        self._statusBarModel.appendColumn(columnStatusBar) # dataChanged is not emited. why?
        self._chartDisplayModel.appendColumn(columnChartDisplay)

        self._statusBarModel.dataChanged.emit(self._statusBarModel.index(0, 0),
                                              self._statusBarModel.index(self._statusBarModel.rowCount()-1,
                                              self._statusBarModel.columnCount()-1),
                                              self._roles_list)


    def _updateStatusList(self):
        """Update the values of the Item List"""
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

        # Set the other parameters.
        self._interestedList.setItemValue('numPars', numPars)
        self._interestedList.setItemValue('numPhases', len(project_dict['phases']))
        self._interestedList.setItemValue('numData', len(project_dict['experiments']))


    def onProjectChanged(self):
        """Define what to do if project dict is changed, e.g. by external library object."""
        self._setModelFromProject()
        # self._statusBarModel.layoutChanged.emit()

    def returnStatusBarModel(self):
        """Return the status bar model."""
        return self._statusBarModel

    def onRefinementDone(self):
        """Define what to do when the refinement done is triggered"""
        self._setModelFromProject()
        self._chartDisplayModel.layoutChanged.emit()

    def returnChartModel(self):
        """Return the chart model"""
        return self._chartDisplayModel