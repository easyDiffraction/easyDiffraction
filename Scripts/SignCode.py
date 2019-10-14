#!/usr/bin/env python3

import os
import sys
import requests
import subprocess
import shutil

# Start
print()
print('***** Variables')
print()

# Os
os_name = sys.argv[1] if len(sys.argv) > 1 else 'osx'
print('os_name:', os_name)

# Password
certificate_password = sys.argv[2] if len(sys.argv) > 2 else ''

# Project
product_name = 'easyDiffraction'
product_url = 'easydiffraction.github.io'
print('product_name:', product_name)
print('product_url:', product_url)

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
dist_dir_path = os.path.join(project_dir_path, 'dist')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)

# Installer related paths
installer_name = product_name + 'Installer'
installer_exe_ext = {
    'osx': '.dmg',
    'windows': '.exe',
    'linux': ''
    }
installer_exe_path = os.path.join(dist_dir_path, installer_name + installer_exe_ext[os_name])
print('installer_name:', installer_name)
print('installer_exe_path:', installer_exe_path)

# Code signing
if (os_name == 'windows'):
    # Signing data
    print()
    print('***** Signing data')
    signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x64', 'signtool.exe')
    certificate_file_path = os.path.join(project_dir_path, 'external', 'ESS_cert.pfx')
    print('signtool_exe_path:', signtool_exe_path)
    print('certificate_file_path:', certificate_file_path)

    # Import certificate
    print()
    print('***** Import certificate')
    args = ['certutil.exe',
            #'-user', # "Current User" Personal store.
            '-p', certificate_password, # the password for the .pfx file
            '-importpfx', certificate_file_path # name of the .pfx file
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    # Code signing
    print()
    print('***** Code signing')
    args = [signtool_exe_path, 'sign', # info - https://msdn.microsoft.com/en-us/data/ff551778(v=vs.71)
            #'/f', certificate_file_path, # signing certificate in a file
            #'/p', certificate_password, # password to use when opening a PFX file
            '/sm', # use a machine certificate store instead of a user certificate store
            '/d', product_name, # description of the signed content
            '/du', product_url, # URL for the expanded description of the signed content
            '/t', 'http://timestamp.digicert.com', # URL to a timestamp server
            '/debug',
            '/v', # display the verbose version of operation and warning messages
            installer_exe_path
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

# End
print()
