import os
import sys
import zipfile
import tempfile
from urllib.parse import urlparse


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
