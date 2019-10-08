#!/usr/bin/env python3

import os
import sys
import subprocess
from distutils.dir_util import copy_tree

# paths
current_dir = os.getcwd()
installer_dir = os.path.join(current_dir, "Installer")
config_xml = os.path.join(installer_dir, "config", "config.xml")
packages_dir = os.path.join(installer_dir, "packages")
data_dir = os.path.join(packages_dir, "io.github.easydiffraction", "data")
examples_dir = os.path.join(current_dir, "Examples")
app = os.path.join(current_dir, "dist", "easyDiffraction.app")

# Copy files/dirs for installer
copy_tree(examples_dir, os.path.join(data_dir, "Examples"))
copy_tree(app, os.path.join(data_dir, "easyDiffraction.app"))

# Create installer
args = ['/Users/andrewsazonov/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator',
        '--verbose',
        '--offline-only',
        '-c', config_xml,
        '-p', packages_dir,
        '-t', '/Users/andrewsazonov/Qt/Tools/QtInstallerFramework/3.1/bin/installerbase',
        'easyDiffractionInstaller'
        ]
#print(args)
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)
