import PyImports.ProjectIO as ProjectIO
import os

from PySide2.QtCore import Qt, QObject, Signal, Slot, QUrl
from PySide2.QtGui import QStandardItem, QStandardItemModel

class ProjectModel(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tempDir = ProjectIO.make_temp_dir()
        self._saveSuccess = False
        self._projectFile = None
        self._isValidCif = None
        self._model = QStandardItemModel()
        self.main_rcif_path = None
        self.name = None
        self.keywords = None
    #     self._role_names_list = ['name', 'keywords', 'phases', 'experiments']
    #     self._roles_list = []
    #     self._roles_dict = {}
    #     self._setRolesListAndDict()
    #
    #
    # def _setRolesListAndDict(self):
    #     """..."""
    #     for i, role_name in enumerate(self._role_names_list):
    #         display_role = self._first_role + i
    #         edit_role = display_role + self._edit_role_increment
    #         self._roles_dict[display_role] = role_name.encode()
    #         self._roles_dict[edit_role] = '{}{}'.format(role_name, self._edit_role_name_suffix).encode()
    #         self._roles_list.append(display_role)
    #         self._roles_list.append(edit_role)

    @Slot(str)
    def loadProject(self, main_rcif_path):
        self.main_rcif_path = QUrl(main_rcif_path).toLocalFile()
        #
        if ProjectIO.check_if_zip(self.main_rcif_path):
            if ProjectIO.check_project_file(self.main_rcif_path):
                _ = ProjectIO.temp_project_dir(self.main_rcif_path, self.tempDir)
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
            f.write('_phases \n')
            f.write('_experiments\n')
        self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')

    @Slot(str)
    def createProject(self, dataDir):
        extension = dataDir[-4:]
        if extension != '.zip':
            saveName = dataDir + '.zip'
        self._projectFile = saveName

    def __exit__(self, exc, value, tb):
        self.tempDir.cleanup()