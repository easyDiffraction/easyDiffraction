import os
import operator
import webbrowser
import logging
from functools import reduce
import zipfile
import tempfile
import urllib
import pathlib

def nested_get(dictionary, keys_list):
    """Access a nested object in root by key sequence."""
    try:
        return reduce(operator.getitem, keys_list, dictionary)
    except:
        return ""


def nested_set(dictionary, keys_list, value):
    """Get a value in a nested object in root by key sequence."""
    nested_get(dictionary, keys_list[:-1])[keys_list[-1]] = value


def find_in_obj(obj, condition, path=None):
    """..."""
    if path is None:
        path = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(path)
            new_path.append(key)
            for result in find_in_obj(value, condition, path=new_path):
                yield result
            if condition == key:
                new_path = list(path)
                new_path.append(key)
                yield new_path


def open_url(url=""):
    """
    Open the given URL in the default system browser
    """
    try:
        webbrowser.open('file://' + os.path.realpath(url))
    except Exception as ex:
        logging.info("Report viewing failed: "+ str(ex))


def get_num_refine_pars(project_dict):
    # Get number of parameters
    numPars = 0
    for path in find_in_obj(project_dict, 'refine'):
        keys_list = path[:-1]
        hide = nested_get(project_dict, keys_list + ['hide'])
        if hide:
            continue
        if nested_get(project_dict, keys_list + ['refine']):
            numPars = numPars + 1
    return numPars


def check_project_dict(project_dict):
    isValid = True
    keys = ['phases', 'experiments', 'calculations']
    # if set(project_dict.keys).intersection([''])
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


def temp_project_dir(filename):
    # Assume we're ok.....
    targetdir = make_temp_dir()
    with zipfile.ZipFile(filename, 'r') as zip:
        zip.extractall(targetdir.name)
    return targetdir


def create_project_zip(data_dir, saveName):

    mustContain = ['main.cif',
                   'phases.cif',
                   'experiments.cif']
    canContain = ['saved_structure.png',
                  'saved_refinement.png']

    saveName = file_uri_to_path(saveName)

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

    return check_project_file(saveName)

def file_uri_to_path(file_uri, path_class=pathlib.PurePath):
    """
    This function returns a pathlib.PurePath object for the supplied file URI.

    :param str file_uri: The file URI ...
    :param class path_class: The type of path in the file_uri. By default it uses
        the system specific path pathlib.PurePath, to force a specific type of path
        pass pathlib.PureWindowsPath or pathlib.PurePosixPath
    :returns: the pathlib.PurePath object
    :rtype: pathlib.PurePath
    """
    windows_path = isinstance(path_class(), pathlib.PureWindowsPath)
    file_uri_parsed = urllib.parse.urlparse(file_uri)
    file_uri_path_unquoted = urllib.parse.unquote(file_uri_parsed.path)
    if windows_path and file_uri_path_unquoted.startswith("/"):
        result = path_class(file_uri_path_unquoted[1:])
    else:
        result = path_class(file_uri_path_unquoted)
    if result.is_absolute() == False:
        raise ValueError("Invalid file uri {} : resulting path {} not absolute".format(
            file_uri, result))
    return result