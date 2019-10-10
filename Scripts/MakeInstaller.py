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
installer_dir_path = os.path.join(project_dir_path, 'Installer')
print('project_dir_path:', project_dir_path)
print('scripts_dir_path:', scripts_dir_path)
print('dist_dir_path:', dist_dir_path)
print('installer_dir_path:', installer_dir_path)

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
config_xml_path = os.path.join(installer_dir_path, 'config', 'config.xml')
packages_dir_path = os.path.join(installer_dir_path, 'packages')
data_dir_path = os.path.join(packages_dir_path, 'io.github.easydiffraction', 'data')
installer_name = project_name + 'Installer'
print('config_xml_path:', config_xml_path)
print('packages_dir_path:', packages_dir_path)
print('data_dir_path:', data_dir_path)

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
print()
print('***** Download QtInstallerFramework installer')
qtifw_installer = requests.get(qtifw_url, allow_redirects=True)
open(qtifw_setup_path, 'wb').write(qtifw_installer.content)

# Attach QtInstallerFramework DMG
if (os_name == 'osx'):
    print()
    print('***** Attach QtInstallerFramework DMG')
    args = ['hdiutil', 'attach', qtifw_setup_path]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

# Fix permissions
if (os_name == 'linux'):
    print()
    print('***** Fix permissions')
    args = ['chmod', 'a+x', qtifw_setup_exe_path[os_name]]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

# Install QtInstallerFramework
print()
print('***** Install QtInstallerFramework silently')
args = [qtifw_setup_exe_path[os_name], '--script', silent_install_script_path]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

if (os_name == 'linux'):
    print()
    print('***** Paths')
    #args = ['ls', '/home']
    #result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    #print(result)
    #args = ['ls', '/home/travis']
    #result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    #print(result)
    # args = ['ls', '/home/travis/Qt']
    # result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # print(result)
    # args = ['ls', '/home/travis/Qt/QtIFW-3.1.1']
    # result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # print(result)
    # args = ['ls', '/home/travis/Qt/QtIFW-3.1.1/bin']
    # result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # print(result)
    args = ['ls', '/home/travis/easyDiffraction']
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
    args = ['ls', '/home/travis/virtualenv']
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)


# Move files/dirs needed for creating installer (freezed app after PyInstaller, Examples folder, etc.)
print()
print('***** Move files/dirs needed for creating installer')
#print('data_dir list (before):', os.listdir(data_dir_path))
os.makedirs(data_dir_path)
shutil.move(examples_dir_path, data_dir_path)
shutil.move(freezed_app_path, data_dir_path)
#print('data_dir list (after):', os.listdir(data_dir_path))

# Create installer from copied files
print()
print('***** Create installer from moved files/dirs')
print()
args = [qtifw_binarycreator,
        '--verbose',
        '--offline-only',
        '-c', config_xml_path,
        '-p', packages_dir_path,
        '-t', qtifw_installerbase,
        installer_name
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

# Create DMG from installer
if (os_name == 'osx'):
    print()
    print('***** Create DMG from installer')
    print()
    installer_app_path = os.path.join(dist_dir_path, installer_name + '.app')
    installer_dmg_path = os.path.join(dist_dir_path, installer_name + '.dmg')
    args = ['hdiutil',
            'create',
            '-volname', project_name,
            '-srcfolder', installer_app_path,
            '-ov', installer_dmg_path
            ]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

# End
print()
