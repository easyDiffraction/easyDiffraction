#!/usr/bin/env python3

import os
import subprocess
import Project

if __name__ == "__main__":
    config = Project.Config()

    os_name = config['os']['name']
    project_name = config['project']['name']
    project_dir_path = config['project']['dir_path']
    distribution_dir = config['project']['subdirs']['distribution']
    distribution_dir_path = os.path.join(project_dir_path, distribution_dir)
    cryspy_path = config['pyinstaller']['lib_path']['cryspy']
    separator = config['pyinstaller']['separator'][os_name]

    Project.run(title='Create dist by pyinstaller', args=[
        'pyinstaller', '{0}/App/{1}.py'.format(project_dir_path, project_name),
        '--name', project_name,                                     # Name to assign to the bundled app and spec file (default: first script’s basename)
        '--noconfirm',                                              # Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
        '--clean',                                                  # Clean PyInstaller cache and remove temporary files before building.
        '--windowed',                                               # Windows and Mac OS X: do not provide a console window for standard i/o.
        '--onedir',                                                 # Create a one-folder bundle containing an executable (default)
        '--log-level', 'WARN',                                      # LEVEL may be one of DEBUG, INFO, WARN, ERROR, CRITICAL (default: INFO).
        '--distpath', "{0}".format(distribution_dir_path),          # Where to put the bundled app (default: ./dist)
        '--workpath', "{0}/.build".format(distribution_dir_path),   # Where to put all the temporary work files, .log, .pyz and etc. (default: ./build)
        '--icon', '{0}/App/QmlImports/{1}/Resources/Icons/App.{2}'.format(project_dir_path, project_name, separator),
        '--add-data', "{0}{1}cryspy".format(cryspy_path, separator),
        '--add-data', "{0}/App{1}.".format(project_dir_path, separator)
        ])

    if os_name == 'osx':
        Project.run(title='Add hidpi support', args=[
            'plutil',
            '-insert', 'NSHighResolutionCapable',
            '-bool', 'YES',
            '{0}/{1}.app/Contents/Info.plist'.format(distribution_dir_path, project_name)
            ])
