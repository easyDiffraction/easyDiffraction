#!/usr/bin/env python3

import os, sys
import shutil
import yaml     # pip3 install pyyaml

import Variables

var = Variables.VarsConfig()

# Read config
config_file_path = os.path.join(os.getcwd(), 'Configs', 'Project.yml')
with open(config_file_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Zip installer
print('\n***** Zip installer')
shutil.make_archive(config['release']['file_path'], 'zip', config['structure']['installer'], var.installer_exe_name)
