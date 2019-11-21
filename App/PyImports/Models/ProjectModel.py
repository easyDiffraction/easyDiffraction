import PyImports.ProjectIO as ProjectIO
import os
import sys
from urllib.parse import urlparse

from PySide2.QtCore import QObject, Slot, QUrl, Signal, Property

class ProjectModel(QObject):

    def __init__(self, projectManager=None, parent=None):
        super().__init__(parent)

        if projectManager is None:
            projectManager = ProjectManager()

        self.tempDir = ProjectIO.make_temp_dir()
        self.manager = projectManager
        self._saveSuccess = False
        self._projectFile = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.name = None
        self.keywords = None

    @Slot(str)
    def loadProject(self, main_rcif_path):
        #
        self.setMain_rcif_path(main_rcif_path)
        #
        if ProjectIO.check_if_zip(self.main_rcif_path):
            if ProjectIO.check_project_file(self.main_rcif_path):
                _ = ProjectIO.temp_project_dir(self.main_rcif_path, self.tempDir)
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
                self.keywords = keywords[1]

        if (self.name is None) or (self.keywords is None):
            self._isValidCif = False

    @Slot(str, str)
    def writeMain(self, name='Undefined', keywords='\'neutron diffraction, powder, 1d\''):
        with open(os.path.join(self.tempDir.name, 'main.cif'), 'w') as f:
            f.write('_name %s\n' % name)
            f.write('_keywords %s\n' % keywords)
            f.write('_phases\n')
            f.write('_experiments\n')
        self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')

    @Slot(str)
    def createProject(self, dataDir):
        extension = dataDir[-4:]
        saveName = dataDir
        if extension != '.zip':
            saveName = dataDir + '.zip'
        self._projectFile = saveName
        self.manager.validSaveState = True

    def setMain_rcif_path(self, rcifPath):
        self._resetOnInitialize()
        FILE = urlparse(rcifPath).path
        if sys.platform.startswith("win"):
            if FILE[0] == '/':
                FILE = FILE[1:].replace('/', os.path.sep)
        self.main_rcif_path = FILE

    def _resetOnInitialize(self):
        # At this point we have an object which needs to be reset.
        self.tempDir.cleanup()
        self.tempDir = ProjectIO.make_temp_dir()
        self.manager.validSaveState = False
        self._saveSuccess = False
        self._projectFile = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.name = None
        self.keywords = None

    def __exit__(self, exc, value, tb):
        self.tempDir.cleanup()

class ProjectManager(QObject):
    projectSaveChange = Signal(bool)

    def __init__(self, parent=None):
        super(ProjectManager, self).__init__(parent)
        self._projectSaveBool = False

    def get_isValidSaveState(self):
        return self._projectSaveBool

    def set_isValidSaveState(self, value):
        if self._projectSaveBool != value:
            self._projectSaveBool = value
            self.projectSaveChange.emit(value)

    validSaveState = Property(bool, get_isValidSaveState, set_isValidSaveState, notify=projectSaveChange)
