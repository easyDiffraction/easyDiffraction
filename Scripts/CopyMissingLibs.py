#!/usr/bin/env python3

import os
import glob, shutil
import Variables

var = Variables.VarsConfig()

print('\n***** Copy missing libraries')
for lib in var.os_specific_missing_libs[var.os_name]:
    lib_path = os.path.join(var.shiboken2_path, lib)
    for file_path in glob.glob(lib_path): # for cases with '*' in the lib name
        print("- source:", file_path)
        print("+ destination:", var.pyside2_path)
        shutil.copy(file_path, var.pyside2_path, follow_symlinks=True)
