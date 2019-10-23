#!/usr/bin/env python3

import os, sys
import requests
import shutil
import subprocess
import Variables

var = Variables.VarsConfig()
qtifw = Variables.InstallerFrameworkConfig(var.os_name, var.scripts_dir_path, var.user_home_dir)

print('\n***** Download QtInstallerFramework installer')
qtifw_installer = requests.get(qtifw.url, allow_redirects=True)
open(qtifw.setup_as_downloaded_path, 'wb').write(qtifw_installer.content)

if (var.os_name == 'osx'):
    print('\n***** Attach QtInstallerFramework DMG')
    args = ['hdiutil', 'attach', qtifw.setup_as_downloaded_path]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)
elif (var.os_name == 'linux'):
    print('\n***** export QT_QPA_PLATFORM=minimal')
    os.environ["QT_QPA_PLATFORM"] = "minimal"
    print('\n***** Fix permissions')
    args = ['chmod', 'a+x', qtifw.setup_exe_path[var.os_name]]
    result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(result)

print('\n***** Install QtInstallerFramework silently')
args = [qtifw.setup_exe_path[var.os_name], '--script', var.silent_install_script_path, '--no-force-installations']
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)

print('\n***** Move files/dirs needed for creating installer')
shutil.rmtree(var.installer_data_dir_path, ignore_errors=True)
os.makedirs(var.installer_data_dir_path)
shutil.move(var.examples_dir_path, var.installer_data_dir_path)
shutil.move(var.freezed_app_path, var.installer_data_dir_path)

print('\n***** Create installer from moved files/dirs')
args = [qtifw.binarycreator_path, '--verbose', '--offline-only',
        '-c', var.installer_config_xml_path,
        '-p', var.installer_packages_dir_path,
        '-t', qtifw.installerbase_path,
        var.installer_exe_path
        ]
result = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
print(result)
