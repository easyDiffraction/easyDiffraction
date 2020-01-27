from PySide2.QtCore import Qt, QObject
from PySide2.QtGui import QStandardItem, QStandardItemModel

import PyImports.Helpers as Helpers
from PyImports.StatusObjects import StatusItem, StatusList
from PyImports.Models.BaseModel import BaseModel

class StatusModel(BaseModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._calculator = None

        # Create the status items
        chiItem = StatusItem('chiSq', title='Current \u03c7\u00b2', additionalData=1)
        chiItem.setReturn(True)
        chiItem.title = 'Previous \u03c7\u00b2'
        chiItem.setReturn(False)
        self._interestedList = StatusList([
            chiItem,
            StatusItem('numPars', title='Fit parameters', additionalData=1),
            StatusItem('numData', title='Experiments', additionalData=0),
            StatusItem('numPhases', title='Phases', additionalData=0)
        ])

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

    def _setRolesListAndDict(self):
        """..."""
        offset = 100
        for i, role_name in enumerate(self._role_names_list):
            display_role = self._first_role + i
            self._roles_dict['status'][display_role] = role_name.encode()
            self._roles_list.append(display_role)
            self._roles_dict['plot'][self._first_role + i + offset] = role_name.encode()

    def _setModelsFromProjectDict(self):
        """Create the initial data list with structure for GUI fitables table."""
        _ = self._statusBarModel.removeColumns(0, self._statusBarModel.columnCount())
        _ = self._chartDisplayModel.removeColumns(0, self._chartDisplayModel.columnCount())

        columnStatusBar = []
        columnChartDisplay = []

        self._updateStatusList()

        for interest in self._interestedList:
            # Add the status bar item
            columnStatusBar.append(self._makeItem(interest, self._roles_dict['status'].items()))
            # Does this need to added to the plot?
            if interest.additionalData == 1:
                columnChartDisplay.append(self._makeItem(interest, self._roles_dict['plot'].items()))

            # Does this item also have previous values which need to be shown?
            if interest.hasPrevious:
                interest.setReturn(True)
                if interest.value is not None:
                    columnStatusBar.append(self._makeItem(interest, self._roles_dict['status'].items()))
                interest.setReturn(False)

        # Set the models
        self._statusBarModel.appendColumn(columnStatusBar)
        self._chartDisplayModel.appendColumn(columnChartDisplay)

        self._statusBarModel.dataChanged.emit(self._statusBarModel.index(0, 0),
                                              self._statusBarModel.index(self._statusBarModel.rowCount()-1,
                                              self._statusBarModel.columnCount()-1),
                                              self._roles_list)


    def _updateStatusList(self):
        """Update the values of the Item List"""
        project_dict = self._project_dict

        # Set chi squared
        try:
            self._interestedList.setItemValue('chiSq', round(project_dict['info']['chi_squared'].value, 2))
        except KeyError:
            self._interestedList.setItemValue('chiSq', 0)


        # Get number of parameters
        numPars = Helpers.get_num_refine_pars(project_dict.asDict())

        # Set the other parameters.
        self._interestedList.setItemValue('numPars', numPars)
        self._interestedList.setItemValue('numPhases', len(project_dict['phases']))
        self._interestedList.setItemValue('numData', len(project_dict['experiments']))

    def returnStatusBarModel(self):
        """Return the status bar model."""
        return self._statusBarModel

    def onRefinementDone(self):
        """Define what to do when the refinement done is triggered"""
        self._setModelsFromProjectDict()
        self._chartDisplayModel.layoutChanged.emit()

    def returnChartModel(self):
        """Return the chart model"""
        return self._chartDisplayModel

    @staticmethod
    def _makeItem(thisInterest, theseItems):
        """Make an item. This can be a plot or status bar"""
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
