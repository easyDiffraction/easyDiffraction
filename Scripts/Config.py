#!/usr/bin/env python3

import os, sys
import yaml # pip3 install pyyaml
import PySide2, shiboken2 # pip3 install pyside2

# CLASS

class Config:
    def __init__(self):
        self._config_dir = os.getcwd()
        self._config_name = 'Project.yml'
        self._config = self._loadYaml(self._config_dir, self._config_name)
        self._config['project']['dir'] = self._config_dir
        self._config['os']['name'] = self._osName()
        self._config['pyinstaller']['lib_path']['shiboken2'] = shiboken2.__path__[0]
        self._config['pyinstaller']['lib_path']['pyside2'] = PySide2.__path__[0]

    def __repr__(self):
        return yaml.dump(self._config, sort_keys=False, indent=2, allow_unicode=True)

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
