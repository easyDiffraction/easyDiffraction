#!/usr/bin/env python3

import os
import glob, shutil
import PySide2, shiboken2

import Variables

var = Variables.VarsConfig()

if __name__ == "__main__":

shiboken2_path = shiboken2.__path__[0]
pyside2_path = PySide2.__path__[0]

print('\n***** Copy missing libraries')
for lib in var.os_specific_missing_libs[var.os_name]:
    lib_path = os.path.join(shiboken2_path, lib)
    for file_path in glob.glob(lib_path): # for cases with '*' in the lib name
        print("- source:", file_path)
        print("+ destination:", pyside2_path)
        shutil.copy(file_path, pyside2_path, follow_symlinks=True)
