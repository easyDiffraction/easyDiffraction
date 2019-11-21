#!/usr/bin/env python3

import os, sys
import requests
import shutil
import Project

if __name__ == "__main__":
    config = Project.Config()
    os_name = config['os']['name']
    project_dir_path = config['project']['dir_path']
    scripts_dir_path = config['project']['subdirs']['scripts']['path']
    examples_dir_path = config['project']['subdirs']['examples']['path']
    silent_install_script = config['scripts']['silent_install']
    freezed_app_path = config['app']['freezed_path']
    qtifw_installerbase_path = config['qtifw']['installerbase_path']
    qtifw_binarycreator_path = config['qtifw']['binarycreator_path']
    qtifw_setup_download_url = config['qtifw']['setup']['download_url']
    qtifw_setup_exe_path = config['qtifw']['setup']['exe_path']
    qtifw_setup_download_path = config['qtifw']['setup']['download_path']
    installer_data_dir_path = config['app']['installer']['data_dir_path']
    installer_config_xml_path = config['app']['installer']['config_xml_path']
    installer_packages_dir_path = config['app']['installer']['packages_dir_path']
    installer_exe_path = config['app']['installer']['exe_path']

    Project.printTitle('Download QtInstallerFramework installer')
    qtifw_installer = requests.get(qtifw_setup_download_url, allow_redirects=True)
    open(qtifw_setup_download_path, 'wb').write(qtifw_installer.content)

    if os_name == 'osx':
        Project.printTitle('Attach QtInstallerFramework DMG')
        Project.run('hdiutil', 'attach', config['qtifw']['setup']['download_path'])
    elif os_name == 'linux':
        Project.printTitle('export QT_QPA_PLATFORM=minimal')
        os.environ["QT_QPA_PLATFORM"] = "minimal"
        Project.printTitle('Fix permissions')
        Project.run('chmod', 'a+x', config['qtifw']['setup']['exe_path'])

    Project.printTitle('Install QtInstallerFramework silently')
    Project.run(
        qtifw_setup_exe_path,
        '--script', silent_install_script,
        '--no-force-installations'
        )

    Project.printTitle('Move files/dirs needed for creating installer')
    shutil.rmtree(installer_data_dir_path, ignore_errors=True)
    os.makedirs(installer_data_dir_path)
    shutil.move(examples_dir_path, installer_data_dir_path)
    shutil.move(freezed_app_path, installer_data_dir_path)

    Project.printTitle('Create installer from moved files/dirs')
    Project.run(
        qtifw_binarycreator_path,
        '--verbose',
        '--offline-only',
        '-c', installer_config_xml_path,
        '-p', installer_packages_dir_path,
        '-t', qtifw_installerbase_path,
        installer_exe_path
    )
