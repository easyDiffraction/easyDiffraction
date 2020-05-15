import os
import sys
import tempfile
import zipfile
from typing import Tuple, List

import numpy as np
from datetime import datetime
from pathlib import Path
from urllib.parse import *

from PySide2.QtCore import QObject, Slot, Signal, Property
from easyInterface.Diffraction import DEFAULT_FILENAMES


class ProjectControl(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.tempDir = make_temp_dir()
        self.manager = ProjectManager()
        self._saveSuccess = False
        self._project_file = None
        self._isValidCif = None
        self.project_rcif_path = None
        self.phases_rcif_path = None
        self.experiment_rcif_path = None
        self.experiment_file_format = "cif"
        self._cif_string = None

    @property
    def project_file(self):
        return self._project_file

    @project_file.setter
    def project_file(self, value: str):
        self._project_file = value

    @Slot(str)
    def loadPhases(self, phases_rcif_path: str):
        """
        Load a structure from a file.
        :param phases_rcif_path: URI to phase (r)cif file
        :return:
        """
        self.phases_rcif_path = self.generalizePath(phases_rcif_path)

    @Slot(str)
    def loadExperiment(self, experiment_rcif_path):
        """
        Load an experiment information from a file.
        :param experiment_rcif_path: URI to experiment (r)cif file
        :return:
        """
        self.experiment_rcif_path = self.generalizePath(experiment_rcif_path)
        _, file_ext = os.path.splitext(self.experiment_rcif_path)

        if file_ext == ".cif":
            self.experiment_file_format = "cif"
        elif file_ext == ".xye" or file_ext == ".dat":
            self.experiment_file_format = "xye"

            data = np.loadtxt(self.experiment_rcif_path)
            joined = [" ".join(item) for item in data.astype(str)]
            data_string = "\n".join(joined)

            n_columns_unpolarized = 3
            n_columns_polarized = 5

            # Determine if the loaded data set is polarized or unpolarized
            if data.shape[1] == n_columns_unpolarized:
                self._cif_string = UNPOLARIZED_CIF_HEADER + data_string
            elif data.shape[1] == n_columns_polarized:
                self._cif_string = POLARIZED_CIF_HEADER + data_string
            else:
                raise IOError("Given file did not contain 3 or 5 columns of data.")

        else:
            raise IOError(f"Given file format .{file_ext} is not supported")

    @Slot(str)
    def loadProject(self, project_rcif_path):
        """
        Load a project from a file. The project_rcif_path variable can be a URI to project.cif or a project zip file
        :param project_rcif_path: URI to main.rcif or project.zip
        :return:
        """
        #
        self.set_project_rcif_path(project_rcif_path)
        #
        if check_if_zip(self.project_rcif_path):
            # This is if we've loaded a `zip`
            if check_project_file(self.project_rcif_path):
                _ = temp_project_dir(self.project_rcif_path, self.tempDir)
                self._project_file = self.project_rcif_path
                self.manager.validSaveState = True
                self.project_rcif_path = os.path.join(self.tempDir.name, DEFAULT_FILENAMES['project'])
        else:
            # This is if we have loaded a `cif`
            self.manager.validSaveState = False

        self._isValidCif = True

        with open(self.project_rcif_path, 'r') as f:
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
    def writeMain(self, name='Undefined', keywords='neutron powder diffraction, 1d'):
        """
        Writes a project.cif file in the temp file location.
        :param string name: What is the project name
        :param string keywords: Keywords associated withe the project for easy finding
        :return:
        """
        if isinstance(keywords, str):
            if keywords[0] == '\'':
                keywords = keywords[1:-1]
            keywords = keywords.split(', ')

        with open(os.path.join(self.tempDir.name, DEFAULT_FILENAMES['project']), 'w') as f:
            f.write('_name %s\n' % name)
            f.write('_keywords %s\n' % '\'%s\'' % ', '.join(keywords))
            f.write('_samples\n')
            f.write('_experiments\n')
            f.write('_calculations\n')
        self.project_rcif_path = os.path.join(self.tempDir.name, DEFAULT_FILENAMES['project'])
        self.manager.projectName = name
        self.manager.projectKeywords = keywords
        self.manager.projectModified = datetime.now()

    @Slot(str)
    def createProject(self, data_dir: str):
        """
        Set a project name so that when saving, a project can be created/updated
        :param string data_dir: String corresponding to a save file with full path
        :return:
        """
        extension = data_dir[-4:]
        save_name = data_dir
        if extension != '.zip':
            save_name = data_dir + '.zip'
        self._project_file = save_name
        self.manager.validSaveState = True

    @Slot(str, result=str)
    def fullFilePath(self, f_name: str):
        """
        Return the full file path as a uri for the GUI
        :param f_name: string name of file
        :return: string with base path + file encoded as a URI
        """
        f_path = os.path.join(self.get_project_dir_absolute_path(), f_name)
        f_URI = os.path.join(self.get_project_url_absolute_path(), f_name)
        if os.path.isfile(f_path):
            return f_URI
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
        if self.project_rcif_path:
            return os.path.dirname(os.path.abspath(self.project_rcif_path))
        return ""

    def get_project_url_absolute_path(self) -> str:
        """
        Get the project path as a folder reference
        :return: URI path directory to a folder containing the main rcif
        """
        if self.project_rcif_path:
            FILE = Path(self.get_project_dir_absolute_path()).as_uri()
            if sys.platform.startswith("win") and FILE[0] == '/':
                FILE = FILE[1:].replace('/', os.path.sep)
            return FILE
        return ""

    def set_project_rcif_path(self, rcif_path: str):
        """
        Set the main rcif file path. This is where the project is read from
        :param URI rcif_path: URI to the project.cif file
        :return:
        """
        self._resetOnInitialize()
        self.project_rcif_path = self.generalizePath(rcif_path)

    def generalizePath(self, rcif_path: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        filename = urlparse(rcif_path).path
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
        self.project_rcif_path = None
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

def check_project_dict(project_dict) -> bool:
    is_valid = True
    keys = ['phases', 'experiments', 'calculations']
    if len(set(project_dict.keys()).difference(set(keys))) > 0:
        return False
    for key in keys:
        if not project_dict[key]:
            is_valid = False
    return is_valid


def check_if_zip(filename: str) -> bool:
    return zipfile.is_zipfile(filename)


def check_project_file(filename: str) -> bool:
    is_valid = True
    must_contain = [DEFAULT_FILENAMES['project'], DEFAULT_FILENAMES['phases'], DEFAULT_FILENAMES['experiments']]

    if check_if_zip(filename):
        with zipfile.ZipFile(filename, 'r') as zip:
            list_list = zip.namelist()
            for file in must_contain:
                if file not in list_list:
                    is_valid = False
    else:
        raise TypeError

    return is_valid


def make_temp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory()


def temp_project_dir(filename: str, target_dir=None) -> tempfile.TemporaryDirectory:
    # Assume we're ok.....
    if target_dir is None:
        target_dir = make_temp_dir()
    with zipfile.ZipFile(filename, 'r') as zip:
        zip.extractall(target_dir.name)
    return target_dir


def create_empty_project(data_dir: str, save_name: str) -> str:
    extension = save_name[-4:]
    if extension != '.zip':
        save_name = save_name + '.zip'

    must_contain = [DEFAULT_FILENAMES['project']]
    can_contain = []

    write_zip(data_dir, save_name, must_contain, can_contain)
    return save_name


def create_project_zip(data_dir, save_name) -> Tuple[bool, str]:
    extension = save_name[-4:]
    if extension != '.zip':
        save_name = save_name + '.zip'

    must_contain = [DEFAULT_FILENAMES['project'],
                    DEFAULT_FILENAMES['phases'],
                    DEFAULT_FILENAMES['experiments'],
                    DEFAULT_FILENAMES['calculations']]

    can_contain = ['structure.png',
                   'refinement.png']

    save_name = write_zip(data_dir, save_name, must_contain, can_contain)

    return check_project_file(save_name), save_name


def write_zip(data_dir: str, save_name: str, must_contain: List, can_contain: List) -> str:
    save_name = urlparse(save_name).path
    if sys.platform.startswith("win") and save_name[0] == '/':
        save_name = save_name[1:].replace('/', os.path.sep)

    with zipfile.ZipFile(save_name, 'w') as zip:
        for file in must_contain:
            full_file = os.path.join(data_dir, file)
            if os.path.isfile(full_file):
                zip.write(os.path.join(data_dir, file), file)
            else:
                raise FileNotFoundError
        for file in can_contain:
            full_file = os.path.join(data_dir, file)
            if os.path.isfile(full_file):
                zip.write(full_file, file)
    return save_name


def writeProject(project_model, save_name: str):
    allOK, save_name = create_project_zip(project_model.tempDir.name, save_name)
    project_model._saveSuccess = True
    project_model._project_file = save_name
    if not allOK:
        raise FileNotFoundError


def writeEmptyProject(project_model, save_name: str):
    save_name = create_empty_project(project_model.tempDir.name, save_name)
    project_model._saveSuccess = True
    project_model._project_file = save_name


UNPOLARIZED_CIF_HEADER = """
data_pd

_setup_wavelength      2.00
_setup_offset_2theta   0.00

_pd_instr_resolution_u  0.15000
_pd_instr_resolution_v -0.30000
_pd_instr_resolution_w  0.30000
_pd_instr_resolution_x  0.00000
_pd_instr_resolution_y  0.15000

loop_
_pd_background_2theta
_pd_background_intensity
 0.0000         10.0
 180.0000       10.0
 
loop_
_phase_label
_phase_scale
_phase_igsize
PHASE_NAME 1.1328 0.0

loop_
_pd_meas_2theta
_pd_meas_intensity
_pd_meas_intensity_sigma
"""

POLARIZED_CIF_HEADER = """
data_pd

_setup_wavelength      2.40
_setup_field           1.00
_setup_offset_2theta   0.00

_diffrn_radiation_polarization  0.80
_diffrn_radiation_efficiency    1.00

_pd_instr_resolution_u 11.00
_pd_instr_resolution_v -3.00
_pd_instr_resolution_w  1.00
_pd_instr_resolution_x  0.00
_pd_instr_resolution_y  0.00

_chi2_sum True
_chi2_diff True
_chi2_up False
_chi2_down False

loop_
_pd_background_2theta
_pd_background_intensity
10.0 183.0
15.0 189.0
20.0 210.0
35.0 253.0
40.0 258.0
50.0 285.0
60.0 369.0
65.0 385.0
70.0 361.0

loop_
_phase_label
_phase_scale
_phase_igsize
PHASE_NAME 0.15 0.0

loop_
_pd_meas_2theta
_pd_meas_intensity_up
_pd_meas_intensity_up_sigma
_pd_meas_intensity_down
_pd_meas_intensity_down_sigma
"""
