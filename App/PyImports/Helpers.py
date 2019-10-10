import os
import operator
import webbrowser
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
    Open the given URL in the default sytem browser
    """
    try:
        webbrowser.open('file://' + os.path.realpath(url))
    except Exception as ex:
        print("Report viewing failed: "+ str(ex))

