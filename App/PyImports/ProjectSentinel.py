import os
import sys
import tempfile
import zipfile
from urllib.parse import urlparse

from PySide2.QtCore import Qt, QObject, Slot, Signal, Property
from PySide2.QtGui import QStandardItemModel, QStandardItem


class ProjectControl(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tempDir = make_temp_dir()
        self.manager = ProjectManager()
        self._saveSuccess = False
        self._projectFile = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.name = ''
        self.keywords = ''

    @Slot(str)
    def loadProject(self, main_rcif_path):
        """
        Load a project from a file. The main_rcif_path variable can be a URI to main.cif or a project zip file
        :param main_rcif_path: URI to main.rcif or project.zip
        :return:
        """
        #
        self.setMain_rcif_path(main_rcif_path)
        #
        if check_if_zip(self.main_rcif_path):
            if check_project_file(self.main_rcif_path):
                _ = temp_project_dir(self.main_rcif_path, self.tempDir)
                self._projectFile = self.main_rcif_path
                self.manager.set_isValidSaveState(True)
                self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')
        self._isValidCif = True

        with open(self.main_rcif_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if '_name ' in line:
                name = line.split('_name ')
                self.name = name[1]
            elif '_keywords ' in line:
                keywords = line.split('_keywords ')
                self.keywords = keywords[1:]

        if (self.name is None) or (self.keywords is None):
            self._isValidCif = False
        else:
            self.manager.projectName = self.name
            if isinstance(self.keywords, str):
                self.manager.projectKeywords = self.keywords

    @Slot(str, str)
    def writeMain(self, name='Undefined', keywords='\'neutron diffraction, powder, 1d\''):
        """
        Writes a main.cif file in the temp file location.
        :param string name: What is the project name
        :param string keywords: Keywords associated withe the project for easy finding
        :return:
        """
        with open(os.path.join(self.tempDir.name, 'main.cif'), 'w') as f:
            f.write('_name %s\n' % name)
            f.write('_keywords %s\n' % keywords)
            f.write('_phases\n')
            f.write('_experiments\n')
        self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')

    @Slot(str)
    def createProject(self, dataDir):
        '''
        Set a project name so that when saving, a project can be created/updated
        :param string dataDir: String corresponding to a save file with full path
        :return:
        '''
        extension = dataDir[-4:]
        saveName = dataDir
        if extension != '.zip':
            saveName = dataDir + '.zip'
        self._projectFile = saveName
        self.manager.validSaveState = True

    def setMain_rcif_path(self, rcifPath):
        """
        Set the main rcif file path. This is where the project is read from
        :param URI rcifPath: URI to the main.cif file
        :return:
        """
        self._resetOnInitialize()
        FILE = urlparse(rcifPath).path
        if sys.platform.startswith("win"):
            if FILE[0] == '/':
                FILE = FILE[1:].replace('/', os.path.sep)
        self.main_rcif_path = FILE

    def _resetOnInitialize(self):
        """
        When a new project is loaded, information of the previous is lost and the Project is reset
        :return:
        """
        # At this point we have an object which needs to be reset.
        self.tempDir.cleanup()
        self.tempDir = make_temp_dir()
        self.manager.validSaveState = False
        self._saveSuccess = False
        self._projectFile = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.name = None
        self.keywords = None

    def __exit__(self, exc, value, tb):
        self.tempDir.cleanup()

    validCif = Property(bool, lambda self: self._isValidCif, constant=False)
    savedProject = Property(bool, lambda self: self._saveSuccess, constant=False)


class ProjectManager(QObject):
    projectSaveChange = Signal(bool)

    # projectLoadSignal = Signal()

    def __init__(self, parent=None):
        super(ProjectManager, self).__init__(parent)
        self._projectSaveBool = False
        self._projectName = ''
        self._projectKeywords = ''

    #     self._model = QStandardItemModel()
    #     # Interest items
    #     self._interests = {'name': None,
    #                       'keywords': None
    #                       }
    #     # set role names
    #     self._first_role = Qt.UserRole + 1
    #     self._role_names_list = ['label', 'value']
    #     self._roles_list = []
    #     self._roles_dict = {'projectInfo': {}
    #                         }
    #     self._setRolesListAndDict()
    #
    # @property
    # def interests(self):
    #     return self._interests
    #
    # @interests.setter
    # def interests(self, value):
    #     self._interests = value
    #     self._setModelFromDict()
    #     self.projectLoadSignal.emit()
    #
    # def _setRolesListAndDict(self):
    #     """..."""
    #     offset = 100
    #     for i, role_name in enumerate(self._role_names_list):
    #         display_role = self._first_role + i
    #         self._roles_dict['projectInfo'][display_role] = role_name.encode()
    #         self._roles_list.append(display_role)
    #
    # def _setModelFromDict(self):
    #     """Create the initial data list with structure for GUI fitables table."""
    #     self._model.setColumnCount(0) # faster than clear(); clear() crashes app! why?
    #     # set column
    #     column = []
    #     for key in self.interests.keys():
    #         item = QStandardItem()
    #         for role, role_name_bytes in self._roles_dict['projectInfo'].items():
    #             role_name = role_name_bytes.decode()
    #             value = ''
    #             if role_name == 'value':
    #                 if self.interests[key] is not None:
    #                     value = self.interests[key]
    #             elif role_name == 'label':
    #                 value = key
    #             item.setData(value, role)
    #         column.append(item)
    #     # set model
    #     self._model.appendColumn(column) # dataChanged is not emited. why?
    #     self._model.dataChanged.emit(self._model.index(0, 0), self._model.index(self._model.rowCount()-1, self._model.columnCount()-1), self._roles_list)

    def get_isValidSaveState(self):
        return self._projectSaveBool

    def set_isValidSaveState(self, value):
        if self._projectSaveBool != value:
            self._projectSaveBool = value
            self.projectSaveChange.emit(value)

    def get_projectNameChanged(self):
        return self._projectName

    def set_projectNameChanged(self, value):
        self._projectName = value
        self.projectSaveChange.emit(value)

    def get_projectKeywordsChanged(self):
        return self._projectKeywords

    def set_projectKeywordsChanged(self, value):
        self._projectKeywords = value
        self.projectSaveChange.emit(value)

    validSaveState = Property(bool, get_isValidSaveState, set_isValidSaveState, notify=projectSaveChange)
    # projectInfo = Property('QVariant', lambda self: self._model, notify=projectLoadSignal)
    projectName = Property(str, get_projectNameChanged, set_projectNameChanged, notify=projectSaveChange)
    projectKeywords = Property(str, get_projectKeywordsChanged, set_projectKeywordsChanged, notify=projectSaveChange)


def check_project_dict(project_dict):
    isValid = True
    keys = ['phases', 'experiments', 'calculations']
    if len(set(project_dict.keys()).difference(set(keys))) > 0:
        return False
    for key in keys:
        if not project_dict[key]:
            isValid = False
    return isValid


def check_if_zip(filename):
    return zipfile.is_zipfile(filename)


def check_project_file(filename):
    isValid = True
    mustContain = ['main.cif', 'phases.cif', 'experiments.cif']

    if check_if_zip(filename):
        with zipfile.ZipFile(filename, 'r') as zip:
            listList = zip.namelist()
            for file in mustContain:
                if file not in listList:
                    isValid = False
    else:
        raise TypeError

    return isValid


def make_temp_dir():
    return tempfile.TemporaryDirectory()


def temp_project_dir(filename, targetdir=None):
    # Assume we're ok.....
    if targetdir is None:
        targetdir = make_temp_dir()
    with zipfile.ZipFile(filename, 'r') as zip:
        zip.extractall(targetdir.name)
    return targetdir


def create_project_zip(data_dir, saveName):
    extension = saveName[-4:]
    if extension != '.zip':
        saveName = saveName + '.zip'

    mustContain = ['main.cif',
                   'phases.cif',
                   'experiments.cif']

    canContain = ['saved_structure.png',
                  'saved_refinement.png']

    saveName = urlparse(saveName).path
    if sys.platform.startswith("win"):
        if saveName[0] == '/':
            saveName = saveName[1:].replace('/', os.path.sep)

    with zipfile.ZipFile(saveName, 'w') as zip:

        for file in mustContain:
            fullFile = os.path.join(data_dir, file)
            if os.path.isfile(fullFile):
                zip.write(os.path.join(data_dir, file), file)
            else:
                raise FileNotFoundError
        for file in canContain:
            fullFile = os.path.join(data_dir, file)
            if os.path.isfile(fullFile):
                zip.write(fullFile, file)

    return check_project_file(saveName), saveName


def writeProject(projectModel, saveName):
    allOK, saveName = create_project_zip(projectModel.tempDir.name, saveName)
    projectModel._saveSuccess = True
    projectModel._projectFile = saveName
    if not allOK:
        raise FileNotFoundError
