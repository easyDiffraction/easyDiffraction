#!/usr/bin/env python3

import os
import sys
import subprocess
import Variables

var = Variables.VarsConfig()

print('\n***** Create dist by pyinstaller')
args = ['pyinstaller', '{0}/App/{1}.py'.format(var.project_dir_path, var.project_name),
        '--name', var.project_name, # Name to assign to the bundled app and spec file (default: first script’s basename)
        '--noconfirm',              # Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
        '--clean',                  # Clean PyInstaller cache and remove temporary files before building.
        '--windowed',               # Windows and Mac OS X: do not provide a console window for standard i/o.
        '--onedir',                 # Create a one-folder bundle containing an executable (default)
        '--log-level', 'WARN',      # LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
        '--add-data', "{0}{1}cryspy".format(var.cryspy_path, var.os_specific_separator[var.os_name]),
        '--add-data', "{0}/App{1}.".format(var.project_dir_path, var.os_specific_separator[var.os_name]),
        '--icon', '{0}/App/QmlImports/{1}/Resources/Icons/App.{2}'.format(var.project_dir_path, var.project_name, var.os_specific_icon_ext[var.os_name]),
        '--distpath', "{0}/dist".format(var.project_dir_path), # Where to put the bundled app (default: ./dist)
        '--workpath', "{0}/build".format(var.project_dir_path) # Where to put all the temporary work files, .log, .pyz and etc. (default: ./build)
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

if (var.os_name == 'osx'):
    print('\n***** Add hidpi support')
    args = ['plutil',
            '-insert', 'NSHighResolutionCapable',
            '-bool', 'YES',
            '{0}/{1}.app/Contents/Info.plist'.format(var.dist_dir_path, var.project_name)
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
