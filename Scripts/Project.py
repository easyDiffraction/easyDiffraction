#!/usr/bin/env python3

import os, sys
import subprocess
import yaml # pip install pyyaml
import cryspy # pip install cryspy
import PySide2, shiboken2 # pip install pyside2

# FUNCTIONS

def printTitle(title):
    #print('{0}***** {1}'.format(os.linesep, title))
    print('***** {0}'.format(title))

def run(*args):
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
        # load external config
        self.__dict__ = self._loadYaml(self._config_dir, self._config_name)
        # project
        self.__dict__['project']['dir_path'] = os.getcwd() # ??? self._config_dir
        self.__dict__['project']['subdirs']['distribution']['path'] = self._absolutePath(self.__dict__['project']['subdirs']['distribution']['name'])
        self.__dict__['project']['subdirs']['scripts']['path'] = self._absolutePath(self.__dict__['project']['subdirs']['scripts']['name'])
        self.__dict__['project']['subdirs']['certificates']['path'] = self._absolutePath(self.__dict__['project']['subdirs']['certificates']['name'])
        self.__dict__['project']['subdirs']['examples']['path'] = self._absolutePath(self.__dict__['project']['subdirs']['examples']['name'])
        self.__dict__['os']['name'] = self._osName()
        # scripts
        self.__dict__['scripts']['silent_install'] = os.path.join(self.__dict__['project']['subdirs']['scripts']['path'], 'SilentInstall.js')
        # scripts
        self.__dict__['certificate']['path'] = os.path.join(self.__dict__['project']['subdirs']['certificates']['path'], self.__dict__['certificate']['name'][self._osName()])
        self.__dict__['certificate']['zip_path'] = os.path.join(self.__dict__['project']['subdirs']['certificates']['path'], 'codesigning.zip')
        # application
        self.__dict__['app']['freezed_path'] = os.path.join(self.__dict__['project']['subdirs']['distribution']['path'], self.__dict__['app']['name'] + self.__dict__['app']['freezed_ext'][self._osName()])
        # user
        self.__dict__['user']['home_dir'] = os.path.expanduser('~')
        # freeze app
        self.__dict__['pyinstaller']['lib_path']['cryspy'] = cryspy.__path__[0]
        self.__dict__['pyinstaller']['lib_path']['shiboken2'] = shiboken2.__path__[0]
        self.__dict__['pyinstaller']['lib_path']['pyside2'] = PySide2.__path__[0]
        # installer framework
        self.__dict__['qtifw']['setup']['name'] = '{0}.{1}'.format(self.__dict__['qtifw']['setup']['base'][self._osName()], self.__dict__['qtifw']['setup']['ext'][self._osName()])
        self.__dict__['qtifw']['setup']['download_url'] = 'https://download.qt.io/official_releases/qt-installer-framework/{0}/{1}'.format(self.__dict__['qtifw']['version'], self.__dict__['qtifw']['setup']['name'])
        self.__dict__['qtifw']['setup']['download_path'] = os.path.join(self.__dict__['project']['subdirs']['distribution']['path'], self.__dict__['qtifw']['setup']['name'])
        self.__dict__['qtifw']['setup']['exe_path'] = self._qtifwExe(self._osName())
        self.__dict__['qtifw']['bin_dir_path'] = self._binDirPath(self._osName())
        self.__dict__['qtifw']['binarycreator_path'] = os.path.join(self.__dict__['qtifw']['bin_dir_path'], 'binarycreator')
        self.__dict__['qtifw']['installerbase_path'] = os.path.join(self.__dict__['qtifw']['bin_dir_path'], 'installerbase')
        # app installer
        self.__dict__['app']['installer']['config_dir_path'] = os.path.join(self.__dict__['project']['dir_path'], 'Installer')
        self.__dict__['app']['installer']['config_xml_path'] = os.path.join(self.__dict__['app']['installer']['config_dir_path'], 'config', 'config.xml')
        self.__dict__['app']['installer']['packages_dir_path'] = os.path.join(self.__dict__['app']['installer']['config_dir_path'], 'packages')
        self.__dict__['app']['installer']['data_dir_path'] = os.path.join(self.__dict__['app']['installer']['packages_dir_path'], 'io.github.easydiffraction', 'data')
        self.__dict__['app']['installer']['dir_path'] = self.__dict__['project']['subdirs']['distribution']['path']
        self.__dict__['app']['installer']['name'] = self.__dict__['app']['name'] + 'Installer'
        self.__dict__['app']['installer']['exe_name'] = self.__dict__['app']['installer']['name'] + self.__dict__['os']['gui_exe_ext'][self._osName()]
        self.__dict__['app']['installer']['exe_path'] = os.path.join(self.__dict__['app']['installer']['dir_path'], self.__dict__['app']['installer']['exe_name'])

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

    def _absolutePath(self, relative_path):
        project_dir_path = self.__dict__['project']['dir_path']
        return os.path.join(project_dir_path, relative_path)

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

    def _qtifwExe(self, os_name):
        d = {
            'osx': '/Volumes/{0}/{0}.app/Contents/MacOS/{0}'.format(self.__dict__['qtifw']['setup']['base'][os_name]),
            'windows': self.__dict__['qtifw']['setup']['download_path'],
            'linux': self.__dict__['qtifw']['setup']['download_path']
        }
        return d[os_name]

    def _binDirPath(self, os_name):
        d = {
            'osx': '{0}/Qt/QtIFW-{1}/bin'.format(self.__dict__['user']['home_dir'], self.__dict__['qtifw']['version']),
            'windows': 'C:\\Qt\\QtIFW-{0}\\bin'.format(self.__dict__['qtifw']['version']),
            'linux': '{0}/Qt/QtIFW-{1}/bin'.format(self.__dict__['user']['home_dir'], self.__dict__['qtifw']['version'])
        }
        return d[os_name]

    def getVal(self, *keys):
        current_level = self.__dict__
        for key in keys:
            if key in current_level:
                current_level = current_level[key]
            else:
                return None
        return current_level

# MAIN

if __name__ == "__main__":
    print(Config())
