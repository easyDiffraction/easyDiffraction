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
format = 'zip'
input_dir = config['structure']['installer']
input_name = var.installer_exe_name
output_path = config['release']['file_path'].replace('.zip', '')
shutil.make_archive(output_path, format, input_dir, input_name)
