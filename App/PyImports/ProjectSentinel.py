import os
import sys
import tempfile
import zipfile
import numpy as np
from datetime import datetime
from pathlib import Path
from urllib.parse import *

from PySide2.QtCore import QObject, Slot, Signal, Property


class ProjectControl(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tempDir = make_temp_dir()
        self.manager = ProjectManager()
        self._saveSuccess = False
        self._project_file = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.phases_rcif_path = None
        self.experiment_rcif_path = None

    @Slot(str)
    def loadPhases(self, phases_rcif_path):
        """
        Load a structure from a file.
        :param structure_rcif_path: URI to structure (r)cif file
        :return:
        """
        self.phases_rcif_path = self.generalizePath(phases_rcif_path)

        pass

    @Slot(str)
    def loadExperiment(self, experiment_rcif_path):
        """
        Load an experiment information from a file.
        :param experiment_rcif_path: URI to experiment (r)cif file
        :return:
        """
        self.experiment_rcif_path = self.generalizePath(experiment_rcif_path)

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
            # This is if we've loaded a `zip`
            if check_project_file(self.main_rcif_path):
                _ = temp_project_dir(self.main_rcif_path, self.tempDir)
                self._project_file = self.main_rcif_path
                self.manager.validSaveState = True
                self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')
        else:
            # This is if we have loaded a `cif`
            self.manager.validSaveState = False

        self._isValidCif = True

        with open(self.main_rcif_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if '_name ' in line:
                name = line.split('_name ')
                self.manager.projectName = name[1]
            elif '_keywords ' in line:
                keywords = line.split('_keywords ')
                self.manager.projectKeywords = keywords[1].split('\'')[1].split(', ')

        if (self.manager.projectName is None) or (self.manager.projectKeywords is None):
            self._isValidCif = False
            self.manager.validSaveState = False

    @Slot(str, str)
    def writeMain(self, name='Undefined', keywords='neutron diffraction, powder, 1d'):
        """
        Writes a main.cif file in the temp file location.
        :param string name: What is the project name
        :param string keywords: Keywords associated withe the project for easy finding
        :return:
        """
        if isinstance(keywords, str):
            if keywords[0] == '\'':
                keywords = keywords[1:-1]
            keywords = keywords.split(', ')

        with open(os.path.join(self.tempDir.name, 'main.cif'), 'w') as f:
            f.write('_name %s\n' % name)
            f.write('_keywords %s\n' % '\'%s\'' % ', '.join(keywords))
            f.write('_phases\n')
            f.write('_experiments\n')
        self.main_rcif_path = os.path.join(self.tempDir.name, 'main.cif')
        self.manager.projectName = name
        self.manager.projectKeywords = keywords
        self.manager.projectModified = datetime.now()

    @Slot(str)
    def createProject(self, dataDir):
        """
        Set a project name so that when saving, a project can be created/updated
        :param string dataDir: String corresponding to a save file with full path
        :return:
        """
        extension = dataDir[-4:]
        saveName = dataDir
        if extension != '.zip':
            saveName = dataDir + '.zip'
        self._project_file = saveName
        self.manager.validSaveState = True

    @Slot(str, result=str)
    def fullFilePath(self, fname):
        """
        Return the full file path as a uri for the GUI
        :param fname: string name of file
        :return: string with base path + file encoded as a URI
        """
        fpath = os.path.join(self.get_project_dir_absolute_path(), fname)
        fURI = os.path.join(self.get_project_url_absolute_path(), fname)
        if os.path.isfile(fpath):
            return fURI
        return ""

    @Slot(result=str)
    def projectFileNameWithoutExt(self):
        """
        Return the base project file name without extension
        :return: string with base project file name without extension
        """
        if self._project_file is None:
            return "Undefined"
        base_with_ext = os.path.basename(self._project_file)
        base_without_ext = os.path.splitext(base_with_ext)[0]
        return base_without_ext

    def get_project_dir_absolute_path(self):
        """
        Get the project path as a folder reference
        :return: string path directory to a folder containing the main rcif
        """
        if self.main_rcif_path:
            return os.path.dirname(os.path.abspath(self.main_rcif_path))
        return ""

    def get_project_url_absolute_path(self):
        """
        Get the project path as a folder reference
        :return: URI path directory to a folder containing the main rcif
        """
        if self.main_rcif_path:
            FILE = Path(self.get_project_dir_absolute_path()).as_uri()
            if sys.platform.startswith("win"):
                if FILE[0] == '/':
                    FILE = FILE[1:].replace('/', os.path.sep)
            return FILE
        return ""

    def setMain_rcif_path(self, rcifPath):
        """
        Set the main rcif file path. This is where the project is read from
        :param URI rcifPath: URI to the main.cif file
        :return:
        """
        self._resetOnInitialize()
        self.main_rcif_path = self.generalizePath(rcifPath)

    def generalizePath(self, rcifPath):
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        filename = urlparse(rcifPath).path
        if not sys.platform.startswith("win"):
            return filename
        if filename[0] == '/':
            filename = filename[1:].replace('/', os.path.sep)
        return filename

    def _resetOnInitialize(self):
        """
        When a new project is loaded, information of the previous is lost and the Project is reset
        :return:
        """
        # At this point we have an object which needs to be reset.
        self.tempDir.cleanup()
        self.tempDir = make_temp_dir()
        self.manager.resetManager()
        self._saveSuccess = False
        self._project_file = None
        self._isValidCif = None
        self.main_rcif_path = None
        self.structure_rcif_path = None
        self.experiment_rcif_path = None

    def __exit__(self, exc, value, tb):
        self.tempDir.cleanup()

    validCif = Property(bool, lambda self: self._isValidCif, constant=False)
    savedProject = Property(bool, lambda self: self._saveSuccess, constant=False)
    project_dir_absolute_path = Property(str, get_project_dir_absolute_path, constant=False)
    project_url_absolute_path = Property(str, get_project_url_absolute_path, constant=False)


class ProjectManager(QObject):
    projectSaveChange = Signal(bool)
    projectDetailChange = Signal()

    def __init__(self, parent=None):
        super(ProjectManager, self).__init__(parent)
        self._projectSaveBool = False
        self._projectName = None
        self._projectKeywords = None
        self._projectExp = None
        self._projectInstruments = None
        self._modified = datetime.now()

    def get_isValidSaveState(self):
        return self._projectSaveBool

    def set_isValidSaveState(self, value):
        self._projectSaveBool = value
        self.projectSaveChange.emit(value)

    def get_projectNameChanged(self):
        return self._projectName

    def set_projectNameChanged(self, value):
        self._projectName = value
        self.projectDetailChange.emit()

    def get_projectKeywordsChanged(self):
        KEYWORDS = ''
        if self._projectKeywords is not None:
            KEYWORDS = ', '.join(self._projectKeywords)
        return KEYWORDS

    def set_projectKeywordsChanged(self, value):
        self._projectKeywords = value
        self.projectDetailChange.emit()

    def get_projectExperimentsChanged(self):
        return self._projectExp

    def set_projectExperimentsChanged(self, value):
        self._projectExp = value
        self.projectDetailChange.emit()

    def get_projectInstrumentsChanged(self):
        return self._projectInstruments

    def set_projectInstrumentsChanged(self, value):
        self._projectInstruments = value
        self.projectDetailChange.emit()

    def get_projectModifiedChanged(self):
        return self._modified.strftime("%d/%m/%Y, %H:%M")

    def set_projectModifiedChanged(self, value: datetime):
        self._modified = value
        self.projectDetailChange.emit()


    def resetManager(self):
        self._projectSaveBool = False
        self._projectName = None
        self._projectKeywords = None
        self._projectExp = None
        self._projectInstruments = None

    validSaveState = Property(bool, get_isValidSaveState, set_isValidSaveState, notify=projectSaveChange)
    projectName = Property(str, get_projectNameChanged, set_projectNameChanged, notify=projectDetailChange)
    projectKeywords = Property(str, get_projectKeywordsChanged, set_projectKeywordsChanged, notify=projectDetailChange)
    projectExperiments = Property(str, get_projectExperimentsChanged, set_projectExperimentsChanged,
                                  notify=projectDetailChange)
    projectInstruments = Property(str, get_projectInstrumentsChanged, set_projectInstrumentsChanged,
                                  notify=projectDetailChange)
    projectModified = Property(str, get_projectModifiedChanged, set_projectModifiedChanged, notify=projectDetailChange)

## Project output checking

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


def create_empty_project(data_dir, saveName):

    extension = saveName[-4:]
    if extension != '.zip':
        saveName = saveName + '.zip'

    mustContain = ['main.cif']
    canContain = []

    write_zip(data_dir, saveName, mustContain, canContain)
    return saveName


def create_project_zip(data_dir, saveName):
    extension = saveName[-4:]
    if extension != '.zip':
        saveName = saveName + '.zip'

    mustContain = ['main.cif',
                   'phases.cif',
                   'experiments.cif']

    canContain = ['saved_structure.png',
                  'saved_refinement.png']

    saveName = write_zip(data_dir, saveName, mustContain, canContain)

    return check_project_file(saveName), saveName


def write_zip(data_dir, saveName, mustContain, canContain):
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
    return saveName


def writeProject(projectModel, saveName):
    allOK, saveName = create_project_zip(projectModel.tempDir.name, saveName)
    projectModel._saveSuccess = True
    projectModel._project_file = saveName
    if not allOK:
        raise FileNotFoundError

def writeEmptyProject(projectModel, saveName):
    saveName = create_empty_project(projectModel.tempDir.name, saveName)
    projectModel._saveSuccess = True
    projectModel._project_file = saveName
