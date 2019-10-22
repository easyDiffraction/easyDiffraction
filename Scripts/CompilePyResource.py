#!/usr/bin/env python3

import os
import subprocess

# Start
print()
print('***** Variables')
print()

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)

# Compile qrc (qt resource file) into python file
print()
print('***** Compile qt resource file (.qrc) into python resource file (.py)')
print()
args = ['pyside2-rcc',
        '{0}/App/QmlResource.qrc'.format(project_dir_path),
        '-o', '{0}/App/QmlResource.py'.format(project_dir_path), # Write output to file rather than stdout
        '-no-compress' # Disable all compression
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# End
print()
