#!/usr/bin/env python3

import os
import subprocess
from distutils import dir_util
import Project
import Functions

if __name__ == "__main__":
    Functions.printTitle('Freeze app by PyInstaller')

    config = Project.Config()

    os_name = config['os']['name']
    app_name = config['app']['name']
    project_name = config['project']['name']
    project_dir_path = config['project']['dir_path']
    distribution_dir_path = config['project']['subdirs']['distribution']['path']
    cryspy_path = config['pyinstaller']['lib_path']['cryspy']
    icon_ext = config['app']['icon']['ext'][os_name]
    separator = config['pyinstaller']['separator'][os_name]

    Functions.run(
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
    print("+ Succeeded to freeze app")

    if os_name == 'osx':
        Functions.run(
            'plutil',
            '-insert', 'NSHighResolutionCapable',
            '-bool', 'YES',
            '{0}/{1}.app/Contents/Info.plist'.format(distribution_dir_path, app_name)
            )
        print("+ Succeeded to add hidpi support")

    if os_name == 'linux':
        missing_plugins = config['pyinstaller']['missing_plugins'][os_name]
        pyside2_path = config['pyinstaller']['lib_path']['pyside2']
        app_plugins_path = os.path.join(distribution_dir_path, app_name, 'PySide2', 'plugins')

        for relative_dir_path in missing_plugins:
            src_dir_name = os.path.basename(relative_dir_path)
            src_dir_path = os.path.join(pyside2_path, relative_dir_path)
            dst_dir_path = os.path.join(app_plugins_path, src_dir_name)
            print("= source:     ", src_dir_path)
            print("+ destination:", app_plugins_path)
            dir_util.copy_tree(src_dir_path, dst_dir_path)
        print("+ Succeeded to copy missing EGL and GLX plugins")
