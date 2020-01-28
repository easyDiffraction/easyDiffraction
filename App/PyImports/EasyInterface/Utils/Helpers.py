import os
import operator
import webbrowser
import logging
from functools import reduce


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
