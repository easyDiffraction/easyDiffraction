#!/usr/bin/env python3

import os, sys
import yaml  # pip install pyyaml


# CLASSES

class Config:
    def __init__(self, release_config_file_path):
        # load external config
        self.__dict__ = self._loadYaml(release_config_file_path)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return yaml.dump(self.__dict__, sort_keys=False, indent=2, allow_unicode=True)

    def _loadYaml(self, file_path):
        if not os.path.isfile(file_path):
            sys.exit("- Failed to find config '{0}'".format(file_path))
        with open(file_path, 'r') as file:
            file_content = yaml.load(file, Loader=yaml.FullLoader)
            return file_content

    def _absolutePath(self, relative_path):
        project_dir_path = self.__dict__['project']['dir_path']
        return os.path.join(project_dir_path, relative_path)

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
