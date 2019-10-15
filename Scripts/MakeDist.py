#!/usr/bin/env python3

import os
import sys
import cryspy
import subprocess

# Start
print()
print('***** Variables')
print()

# Os
os_name = sys.argv[1] if len(sys.argv) > 1 else 'osx'
print('os_name:', os_name)

# Project
project_name = 'easyDiffraction'
print('project_name:', project_name)

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
dist_dir_path = os.path.join(project_dir_path, 'dist')
cryspy_path = cryspy.__path__[0]
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)
print('cryspy_path:', cryspy_path)

# OS specific parameters
separator = {
    'osx': ':',
    'windows': ';',
    'linux': ':'
    }

icon_ext = {
    'osx': 'icns',
    'windows': 'ico',
    'linux': 'png'
    }
print('separator:', separator[os_name])
print('icon_ext:', icon_ext[os_name])

# Create dist by pyinstaller
print()
print('***** Create dist by pyinstaller')
print()
args = ['pyinstaller', '{0}/App/{1}.py'.format(project_dir_path, project_name),
        '--name', 'easyDifraction', # Name to assign to the bundled app and spec file (default: first script’s basename)
        '--noconfirm', # Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
        '--clean', # Clean PyInstaller cache and remove temporary files before building.
        '--windowed',
        '--onedir', # Create a one-folder bundle containing an executable (default)
        '--log-level', 'WARN', # LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
        '--add-data', "{0}{1}cryspy".format(cryspy_path, separator[os_name]),
        '--add-data', "{0}/App{1}.".format(project_dir_path, separator[os_name]),
        '--icon', '{0}/App/QmlImports/{1}/Resources/Icons/App.{2}'.format(project_dir_path, project_name, icon_ext[os_name]),
        #'--distpath', "{0}/Build".format(project_dir_path), # Where to put the bundled app (default: ./dist)
        '--workpath', "{0}/Tmp".format(project_dir_path) # Where to put all the temporary work files, .log, .pyz and etc. (default: ./build)
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Add hidpi support for macOS
if (os_name == 'osx'):
    print()
    print('***** Add hidpi support')
    print()
    args = ['plutil',
            '-insert', 'NSHighResolutionCapable',
            '-bool', 'YES',
            '{0}/{1}.app/Contents/Info.plist'.format(dist_dir_path, project_name)
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

# End
print()
