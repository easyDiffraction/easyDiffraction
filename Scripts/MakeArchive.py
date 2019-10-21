#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil

# Start
print('\n***** Variables')

# Os
os_name = sys.argv[1] if len(sys.argv) > 1 else 'osx'
print('os_name:', os_name)

# Release number
release_number = sys.argv[2] if len(sys.argv) > 2 else ''
print('release_number:', release_number)

# Project
product_name = 'easyDiffraction'
product_url = 'easydiffraction.github.io'
print('product_name:', product_name)
print('product_url:', product_url)

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
dist_dir_path = os.path.join(project_dir_path, 'dist')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)

# Installer related paths
installer_dir_path = dist_dir_path
installer_name = product_name + 'Installer'
installer_exe_ext = {
    'osx': '.app',
    'windows': '.exe',
    'linux': ''
    }
installer_exe_name = installer_name + installer_exe_ext[os_name]
print('installer_dir_path:', installer_dir_path)
print('installer_name:', installer_name)
print('installer_exe_ext:', installer_exe_ext)
print('installer_exe_name:', installer_exe_name)

# Archive
target_name = '{0}-{1}-v{2}'.format(product_name, os_name, release_number)
target_path = os.path.join(project_dir_path, target_path)
print('target_name:', target_name)
print('target_path:', target_path)

# Zip installer
print('\n***** Zip installer')
shutil.make_archive(target_path, 'zip', installer_dir_path, installer_exe_name)

# End
print()
