#!/usr/bin/env python3

import re
import os
import sys

# Project
project_name = 'easyDiffraction'

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))

# Settings file
settings_file_path = os.path.join(project_dir_path, 'App', 'QmlImports', 'easyDiffraction', 'Settings.qml')

# Find and app version
with open(settings_file_path, 'r') as f:
    file_content = f.read()
    release_number = re.findall('\d+.\d+.\d+', file_content)[0]

# Output
print(release_number)
