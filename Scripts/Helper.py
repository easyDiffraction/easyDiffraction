#!/usr/bin/env python3

import os, sys
import yaml # pip3 install pyyaml

# CLASS

class Helper:
    def __init__(self):
        self._config = self._templateConfig()
        self._config['os']['name'] = self._osName()

    def __repr__(self):
        return yaml.dump(self._config, sort_keys=False, indent=2, allow_unicode=True)

    def _templateConfig(self):
        string = """
            os:
                name: null
            python:
                lib_path:
                    shiboken2: null
                    pyside2: null
        """
        return yaml.load(string, Loader=yaml.FullLoader)

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
    config = Helper()
    print(config)
