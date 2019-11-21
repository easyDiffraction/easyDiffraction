#!/usr/bin/env python3

import os
import subprocess
import Project

if __name__ == "__main__":
    config = Project.Config()

    os_name = config['os']['name']
    app_name = config['app']['name']
    project_name = config['project']['name']
    project_dir_path = config['project']['dir_path']
    distribution_dir_path = config['project']['subdirs']['distribution']['path']
    cryspy_path = config['pyinstaller']['lib_path']['cryspy']
    icon_ext = config['app']['icon']['ext'][os_name]
    separator = config['pyinstaller']['separator'][os_name]

    Project.printTitle('Freeze app by PyInstaller')
    Project.run(
        'pyinstaller', '{0}/App/{1}.py'.format(project_dir_path, project_name),
        '--name', project_name,                                                 # Name to assign to the bundled app and spec file (default: first script’s basename)
        '--noconfirm',                                                          # Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
        '--clean',                                                              # Clean PyInstaller cache and remove temporary files before building.
        '--windowed',                                                           # Windows and Mac OS X: do not provide a console window for standard i/o.
        '--onedir',                                                             # Create a one-folder bundle containing an executable (default)
        '--log-level', 'WARN',                                                  # LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
        '--distpath', "{0}".format(distribution_dir_path),                      # Where to put the bundled app (default: ./dist)
        '--workpath', "{0}/.build".format(distribution_dir_path),               # Where to put all the temporary work files, .log, .pyz and etc. (default: ./build)
        '--add-data', "{0}{1}cryspy".format(cryspy_path, separator),            # Add CrysPy library
        '--add-data', "{0}/App{1}.".format(project_dir_path, separator),        # Add App Pythnon and QML source files
        '--icon', '{0}/App/QmlImports/{1}/Resources/Icons/App.{2}'.format(project_dir_path, project_name, icon_ext)
        )

    if os_name == 'osx':
        Project.printTitle('Add hidpi support')
        Project.run(
            'plutil',
            '-insert', 'NSHighResolutionCapable',
            '-bool', 'YES',
            '{0}/{1}.app/Contents/Info.plist'.format(distribution_dir_path, app_name)
            )
