#!/usr/bin/env python3

import os
import sys
import requests
import subprocess
import distutils

# Start
print()

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.join(scripts_dir_path, '..')
dist_dir_path = os.path.join(project_dir_path, 'dist')
installer_dir_path = os.path.join(project_dir_path, 'Installer')
print('Variables')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)
print('installer_dir_path:', installer_dir_path)

# What to include to installer
examples_dir_path = os.path.join(project_dir_path, 'Examples')
freezed_app_path = os.path.join(project_dir_path, 'dist', 'easyDiffraction.app')
print('examples_dir_path:', examples_dir_path)
print('freezed_app_path:', freezed_app_path)

# Specific scripts
silent_install_script_path = os.path.join(scripts_dir_path, 'SilentInstall.js')
print('silent_install_script_path:', silent_install_script_path)

# Installer related paths
config_xml_path = os.path.join(installer_dir_path, 'config', 'config.xml')
packages_dir_path = os.path.join(installer_dir_path, 'packages')
data_dir_path = os.path.join(packages_dir_path, 'io.github.easydiffraction', 'data')
installer_name = 'easyDiffractionInstaller'
installer_app_path = os.path.join(installer_dir_path, installer_name) + '.app'
installer_dmg_path = os.path.join(dist_dir_path, installer_name) + '.dmg'

print('config_xml_path:', config_xml_path)
print('packages_dir_path:', packages_dir_path)
print('data_dir_path:', data_dir_path)

# QtInstallerFramework
qtifw_version = '3.1.1'
qtifw_setup_base = 'QtInstallerFramework-mac-x64'
qtifw_setup_ext = 'dmg'
qtifw_setup_name = '{}.{}'.format(qtifw_setup_base, qtifw_setup_ext)
qtifw_setup_path = os.path.join(scripts_dir_path, qtifw_setup_name)
qtifw_setup_exe_path = '/Volumes/{0}/{0}.app/Contents/MacOS/{0}'.format(qtifw_setup_base)
qtifw_bin_path = '~/Qt/QtIFW-{0}/bin'.format(qtifw_version)
qtifw_url = 'https://download.qt.io/official_releases/qt-installer-framework/{0}/{1}'.format(qtifw_version, qtifw_setup_name)
qtifw_binarycreator = os.path.join(qtifw_bin_path, 'binarycreator')
qtifw_installerbase = os.path.join(qtifw_bin_path, 'installerbase')
print('qtifw_version:', qtifw_version)
print('qtifw_setup_path:', qtifw_setup_path)
print('qtifw_url:', qtifw_url)
print('qtifw_binarycreator:', qtifw_binarycreator)
print('qtifw_installerbase:', qtifw_installerbase)

# Download
print()
print('Download QtInstallerFramework installer')
qtifw_installer = requests.get(qtifw_url, allow_redirects=True)
open(qtifw_installer_path, 'wb').write(qtifw_installer.content)

# Attach
print()
print('Attach QtInstallerFramework DMG')
args = ['hdiutil', 'attach', qtifw_setup_path]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Install
print('Install QtInstallerFramework silently')
args = [qtifw_setup_exe_path, '--script', silent_install_script_path]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Copy files/dirs for installer
distutils.dir_util.copy_tree(examples_dir_path, os.path.join(data_dir_path, os.path.basename(examples_dir_path)))
distutils.dir_util.copy_tree(freezed_app_path, os.path.join(data_dir_path, os.path.basename(freezed_app_path)))

# Create installer
args = [qtifw_binarycreator,
        '--verbose',
        '--offline-only',
        '-c', config_xml_path,
        '-p', packages_dir_path,
        '-t', qtifw_installerbase,
        'easyDiffractionInstaller'
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Create dmg
args = ['hdiutil',
        'create',
        '-volname', installer_name,
        '-srcfolder', installer_app_path,
        '-ov', installer_dmg_path
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# End
print()
