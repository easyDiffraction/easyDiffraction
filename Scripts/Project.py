#!/usr/bin/env python3

import os, sys
import subprocess
import yaml # pip install pyyaml
import cryspy # pip install cryspy
import PySide2, shiboken2 # pip install pyside2

# FUNCTIONS

def printTitle(title):
    print('{0}***** {1}'.format(os.linesep, title))

def run(title, args):
    printTitle(title)
    result = subprocess.run(
        args,
        #capture_output=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,    # converts the output to a string instead of a byte array.
        #check=True                  # forces the Python method to throw an exception if the underlying process encounters errors
    )
    if result.stdout:
        print("+ Success:{0}{1}".format(os.linesep, result.stdout))
    if result.stderr:
        print("- Fail:{0}{1}".format(os.linesep, result.stderr))
        sys.exit()

# CLASSES

class Config():
    def __init__(self):
        self._config_dir = os.getcwd()
        self._config_name = 'Project.yml'
        self.__dict__ = self._loadYaml(self._config_dir, self._config_name)
        self.__dict__['project']['dir_path'] = os.getcwd()
        self.__dict__['os']['name'] = self._osName()
        self.__dict__['pyinstaller']['lib_path']['cryspy'] = cryspy.__path__[0]
        self.__dict__['pyinstaller']['lib_path']['shiboken2'] = shiboken2.__path__[0]
        self.__dict__['pyinstaller']['lib_path']['pyside2'] = PySide2.__path__[0]

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return yaml.dump(self.__dict__, sort_keys=False, indent=2, allow_unicode=True)

    def _loadYaml(self, file_dir, file_name):
        file_path = os.path.join(file_dir, file_name)
        if not os.path.isfile(file_path):
            sys.exit("- Failed to find config '{0}'".format(file_path))
        with open(file_path, 'r') as file:
            file_content = yaml.load(file, Loader=yaml.FullLoader)
            return file_content

    def _osName(self):
        platform = sys.platform
        if platform.startswith('darwin'):
            return 'osx'
        elif platform.startswith('lin'):
            return 'linux'
        elif platform.startswith('win'):
            return 'windows'
        else:
            print("* Unsupported platform '{0}'".format(platform))
            return None

# MAIN

if __name__ == "__main__":
    print(Config())
