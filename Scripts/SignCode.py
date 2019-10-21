#!/usr/bin/env python3

import os
import sys
import ast
import requests
import subprocess
import shutil
import zipfile

# Start
print('\n***** Variables\n')

# Os
os_name = sys.argv[1] if len(sys.argv) > 1 else 'osx'
print('os_name:', os_name)

#for arg in sys.argv:
#    print(arg)

# Passwords
passwords_dict = ast.literal_eval(sys.argv[2]) if len(sys.argv) > 2 else {'osx':'', 'windows':'', 'zip':''}
certificate_password = passwords_dict[os_name].replace('\\', '')
zip_password = passwords_dict['zip']

# Project
product_name = 'easyDiffraction'
product_url = 'easydiffraction.github.io'
print('product_name:', product_name)
print('product_url:', product_url)

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
dist_dir_path = os.path.join(project_dir_path, 'dist')
certificates_dir_path = os.path.join(project_dir_path, 'Certificates')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)
print('certificates_dir_path:', certificates_dir_path)

# Installer related paths
installer_name = product_name + 'Installer'
installer_exe_ext = {
    'osx': '.app',
    'windows': '.exe',
    'linux': ''
    }
installer_exe_path = os.path.join(dist_dir_path, installer_name + installer_exe_ext[os_name])
print('installer_name:', installer_name)
print('installer_exe_path:', installer_exe_path)

# Certificates related data
certificate_zip_path = os.path.join(certificates_dir_path, 'codesigning.zip')
certificate_file_name = {
    'osx': 'ESS_cert_mac.p12',
    'windows': 'ESS_cert_win.pfx',
    }
certificate_file_path = os.path.join(certificates_dir_path, certificate_file_name[os_name])
print('certificate_zip_path:', certificate_zip_path)
print('certificate_file_path:', certificate_file_path)

# Unzip certificates
with zipfile.ZipFile(certificate_zip_path) as zf:
    zf.extractall(path=certificates_dir_path, pwd=bytes(zip_password, 'utf-8'))

# Sign code
if (os_name == 'osx'):
    keychain = 'build.keychain'
    keychainpassword = 'password'
    identity = 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)'

    print('\n***** Create keychain')
    args = ['security', 'create-keychain', '-p', keychainpassword, keychain]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Set it to be default keychain')
    args = ['security', 'default-keychain', '-s', keychain]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Unlock created keychain')
    args = ['security', 'unlock-keychain', '-p', keychainpassword, keychain]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Import certificate to created keychain')
    args = ['security', 'import', certificate_file_path, '-k', keychain, '-P', certificate_password, '-T', '/usr/bin/codesign']
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Show certificates')
    args = ['security', 'find-identity', '-v']
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Sign code with imported certificate')
    args = ['codesign', '--deep', '--force', '--verbose', '--sign', identity, installer_exe_path]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

elif (os_name == 'windows'):
    print('\n***** Paths')
    signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x86', 'signtool.exe')
    certificate_file_path = os.path.join(project_dir_path, 'Certificates', 'ESS_cert_win.pfx')
    print('signtool_exe_path:', signtool_exe_path)
    print('certificate_file_path:', certificate_file_path)

    print('\n***** Import certificate')
    args = ['certutil.exe',
            #'-user', # "Current User" Personal store.
            '-p', certificate_password, # the password for the .pfx file
            '-importpfx', certificate_file_path # name of the .pfx file
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

    print('\n***** Sign code with imported certificate')
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
