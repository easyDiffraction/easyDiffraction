#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
import shutil
import site
import PySide2
import shiboken2

# Start
print()
print('***** Variables')
print()

# Os
os_name = sys.argv[1] if len(sys.argv) > 1 else 'osx'
print('os_name:', os_name)

# Main paths
shiboken2_path = shiboken2.__path__[0]
pyside2_path = PySide2.__path__[0]
print('shiboken2_path:', shiboken2_path)
print('pyside2_path:', pyside2_path)

# Windows
  # lib not found: shiboken2.abi3.dll dependency of c:\python37\lib\site-packages\PySide2\QtGui.pyd, etc.
  # lib not found: MSVCP140.dll dependency of c:\python37\lib\site-packages\PySide2\libGLESv2.dll, etc.
  # lib not found: api-ms-win-core-winrt-string-l1-1-0.dll dependency of c:\python37\lib\site-packages\PySide2\qt5bluetooth.dll
  # lib not found: api-ms-win-core-winrt-l1-1-0.dll dependency of c:\python37\lib\site-packages\PySide2\qt5bluetooth.dll
# macOS
  # Can not find path ./libshiboken2.abi3.5.13.dylib (needed by /Users/travis/.python-venv/lib/python3.6/site-packages/PySide2/QtCore.abi3.so)

# OS specific libs to copy
libs_list = {
    'osx': ['libshiboken2.abi3.*.dylib'],
    'windows': ['shiboken2.abi3.dll', 'MSVCP140.dll'],
    'linux': []
    }
print('libs_list:', libs_list[os_name])

# Create dist by pyinstaller
print()
print('***** Copy missing libraries')
print()
for lib in libs_list[os_name]:
    lib_path = os.path.join(shiboken2_path, lib)
    for file_path in glob.glob(lib_path): # for cases with '*' in the lib name
        print("- source:", file_path)
        print("+ destination:", pyside2_path)
        shutil.copy(file_path, pyside2_path, follow_symlinks=True)

# End
print()
