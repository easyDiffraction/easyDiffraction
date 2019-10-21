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

# Project
project_name = 'easyDiffraction'
print('project_name:', project_name)

# Main paths
user_home_dir = os.path.expanduser('~')
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))
dist_dir_path = os.path.join(project_dir_path, 'dist')
installer_config_dir_path = os.path.join(project_dir_path, 'Installer')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)
print('installer_config_dir_path:', installer_config_dir_path)

# What to include to installer
examples_dir_path = os.path.join(project_dir_path, 'Examples')
freezed_app_path = os.path.join(dist_dir_path, project_name)
if os_name == 'osx': freezed_app_path += '.app'
print('examples_dir_path:', examples_dir_path)
print('freezed_app_path:', freezed_app_path)

# Specific scripts
silent_install_script_path = os.path.join(scripts_dir_path, 'SilentInstall.js')
print('silent_install_script_path:', silent_install_script_path)

# Installer related paths
config_xml_path = os.path.join(installer_config_dir_path, 'config', 'config.xml')
packages_dir_path = os.path.join(installer_config_dir_path, 'packages')
data_dir_path = os.path.join(packages_dir_path, 'io.github.easydiffraction', 'data')
installer_name = project_name + 'Installer'
installer_exe_ext = {
    'osx': '.app',
    'windows': '.exe',
    'linux': ''
    }
installer_exe_path = os.path.join(dist_dir_path, installer_name + installer_exe_ext[os_name])
print('config_xml_path:', config_xml_path)
print('packages_dir_path:', packages_dir_path)
print('data_dir_path:', data_dir_path)
print('installer_name:', installer_name)
print('installer_exe_path:', installer_exe_path)

# QtInstallerFramework
qtifw_version = '3.1.1'
qtifw_setup_base = {
    'osx': 'QtInstallerFramework-mac-x64',
    'windows': 'QtInstallerFramework-win-x86',
    'linux': 'QtInstallerFramework-linux-x64'
    }
qtifw_setup_ext = {
    'osx': 'dmg',
    'windows': 'exe',
    'linux': 'run'
    }
qtifw_setup_name = '{0}.{1}'.format(qtifw_setup_base[os_name], qtifw_setup_ext[os_name])
qtifw_setup_path = os.path.join(scripts_dir_path, qtifw_setup_name)
qtifw_setup_exe_path = {
    'osx': '/Volumes/{0}/{0}.app/Contents/MacOS/{0}'.format(qtifw_setup_base[os_name]),
    'windows': qtifw_setup_path,
    'linux': qtifw_setup_path
    }
qtifw_bin_path = {
    'osx': '{0}/Qt/QtIFW-{1}/bin'.format(user_home_dir, qtifw_version),
    'windows': 'C:\\Qt\\QtIFW-{0}\\bin'.format(qtifw_version),
    'linux': '{0}/Qt/QtIFW-{1}/bin'.format(user_home_dir, qtifw_version)
    }
qtifw_url = 'https://download.qt.io/official_releases/qt-installer-framework/{0}/{1}'.format(qtifw_version, qtifw_setup_name)
qtifw_binarycreator = os.path.join(qtifw_bin_path[os_name], 'binarycreator')
qtifw_installerbase = os.path.join(qtifw_bin_path[os_name], 'installerbase')
print('qtifw_version:', qtifw_version)
print('qtifw_setup_path:', qtifw_setup_path)
print('qtifw_setup_exe_path:', qtifw_setup_exe_path[os_name])
print('qtifw_url:', qtifw_url)
print('qtifw_binarycreator:', qtifw_binarycreator)
print('qtifw_installerbase:', qtifw_installerbase)

# Download QtInstallerFramework DMG
print('\n***** Download QtInstallerFramework installer')
qtifw_installer = requests.get(qtifw_url, allow_redirects=True)
open(qtifw_setup_path, 'wb').write(qtifw_installer.content)

# OS specific settings
if (os_name == 'osx'):
    print('\n***** Attach QtInstallerFramework DMG')
    args = ['hdiutil', 'attach', qtifw_setup_path]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
elif (os_name == 'linux'):
    print('\n***** Fix permissions')
    args = ['chmod', 'a+x', qtifw_setup_exe_path[os_name]]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
    print('\n***** export QT_QPA_PLATFORM=minimal')
    os.environ["QT_QPA_PLATFORM"] = "minimal"

# Install QtInstallerFramework
print('\n***** Install QtInstallerFramework silently')
args = [qtifw_setup_exe_path[os_name], '--script', silent_install_script_path, '--no-force-installations']
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Move files/dirs needed for creating installer (freezed app after PyInstaller, Examples folder, etc.)
print('\n***** Move files/dirs needed for creating installer')
os.makedirs(data_dir_path)
shutil.move(examples_dir_path, data_dir_path)
shutil.move(freezed_app_path, data_dir_path)

# Create installer from copied files
print('\n***** Create installer from moved files/dirs')
args = [qtifw_binarycreator, '--verbose', '--offline-only',
        '-c', config_xml_path, '-p', packages_dir_path, '-t', qtifw_installerbase,
        installer_exe_path
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# End
print()
