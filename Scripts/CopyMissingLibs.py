#!/usr/bin/env python3

import os
import glob, shutil
import Project

if __name__ == "__main__":
    config = Project.Config()

    os_name = config['os']['name']
    missing_files = config['pyinstaller']['missing_files'][os_name]
    shiboken2_path = config['pyinstaller']['lib_path']['shiboken2']
    pyside2_path = config['pyinstaller']['lib_path']['pyside2']

    Project.printTitle('Copy missing libraries')
    for file_name in missing_files:
        file_path = os.path.join(shiboken2_path, file_name)
        for file_path in glob.glob(file_path): # for cases with '*' in the lib name
            print("= source:     ", file_path)
            print("+ destination:", pyside2_path)
            shutil.copy(file_path, pyside2_path, follow_symlinks=True)
