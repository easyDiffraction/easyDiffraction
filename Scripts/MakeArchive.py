#!/usr/bin/env python3

import os, sys
import shutil
import Variables

var = Variables.VarsConfig()

# Release number
release_number = sys.argv[1] if len(sys.argv) > 1 else ''
print('release_number:', release_number)

# Archive
target_name = '{0}_{1}_v{2}'.format(var.project_name, var.os_name, release_number)
target_path = os.path.join(var.installer_dir_path, target_name)
print('target_name:', target_name)
print('target_path:', target_path)

# Zip installer
print('\n***** Zip installer')
shutil.make_archive(target_path, 'zip', var.installer_dir_path, var.installer_exe_name)
