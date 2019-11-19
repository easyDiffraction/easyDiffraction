#!/usr/bin/env python3

import os, sys
import cryspy, PySide2, shiboken2

class InstallerFrameworkConfig:
    def __init__(self, os_name, setup_dir_path, user_home_dir):
        self.version = '3.1.1'
        self.setup_base = {
            'osx': 'QtInstallerFramework-mac-x64',
            'windows': 'QtInstallerFramework-win-x86',
            'linux': 'QtInstallerFramework-linux-x64'
            }
        self.setup_ext = {'osx': 'dmg', 'windows': 'exe', 'linux': 'run'}
        self.setup_name = '{0}.{1}'.format(self.setup_base[os_name], self.setup_ext[os_name])
        self.setup_as_downloaded_path = os.path.join(setup_dir_path, self.setup_name)
        self.setup_exe_path = {
            'osx': '/Volumes/{0}/{0}.app/Contents/MacOS/{0}'.format(self.setup_base[os_name]),
            'windows': self.setup_as_downloaded_path,
            'linux': self.setup_as_downloaded_path
            }
        self.bin_dir_path = {
            'osx': '{0}/Qt/QtIFW-{1}/bin'.format(user_home_dir, self.version),
            'windows': 'C:\\Qt\\QtIFW-{0}\\bin'.format(self.version),
            'linux': '{0}/Qt/QtIFW-{1}/bin'.format(user_home_dir, self.version)
            }
        self.binarycreator_path = os.path.join(self.bin_dir_path[os_name], 'binarycreator')
        self.installerbase_path = os.path.join(self.bin_dir_path[os_name], 'installerbase')
        self.url = 'https://download.qt.io/official_releases/qt-installer-framework/{0}/{1}'.format(self.version, self.setup_name)

class VarsConfig:
    def __init__(self):
        self.os_name = self.setOsName()
        #
        self.organization_name = 'easyDiffraction'
        self.project_name = 'easyDiffraction'
        self.project_url = 'https://easydiffraction.github.io'
        self.installer_name = self.project_name + 'Installer'
        #
        self.os_specific_separator = {'osx': ':', 'windows': ';', 'linux': ':'}
        self.os_specific_icon_ext = {'osx': 'icns', 'windows': 'ico', 'linux': 'png'}
        self.os_specific_gui_exe_ext = {'osx': '.app', 'windows': '.exe', 'linux': ''}
        self.os_specific_cli_exe_ext = {'osx': '', 'windows': '.exe', 'linux': ''}
        self.os_specific_missing_libs = {
            'osx': ['libshiboken2.abi3.*.dylib'],
            'windows': ['shiboken2.abi3.dll', 'MSVCP140.dll'],
            'linux': []
            }
        #
        self.user_home_dir = os.path.expanduser('~')
        self.scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.project_dir_path = os.path.realpath(os.path.join(self.scripts_dir_path, '..'))
        self.examples_dir_path = os.path.join(self.project_dir_path, 'Examples')
        self.dist_dir_path = os.path.join(self.project_dir_path, 'dist')
        self.freezed_app_path = os.path.join(self.dist_dir_path, self.project_name)
        if self.os_name == 'osx': self.freezed_app_path += '.app'
        #
        self.silent_install_script_path = os.path.join(self.scripts_dir_path, 'SilentInstall.js')
        self.installer_config_dir_path = os.path.join(self.project_dir_path, 'Installer')
        self.installer_config_xml_path = os.path.join(self.installer_config_dir_path, 'config', 'config.xml')
        self.installer_packages_dir_path = os.path.join(self.installer_config_dir_path, 'packages')
        self.installer_data_dir_path = os.path.join(self.installer_packages_dir_path, 'io.github.easydiffraction', 'data')
        self.installer_dir_path = self.dist_dir_path
        self.installer_exe_name = self.installer_name + self.os_specific_gui_exe_ext[self.os_name]
        self.installer_exe_path = os.path.join(self.installer_dir_path, self.installer_exe_name)
        #
        self.certificates_dir_path = os.path.join(self.project_dir_path, 'Certificates')
        self.certificates_zip_path = os.path.join(self.certificates_dir_path, 'codesigning.zip')
        self.certificate_file_name = {'osx': 'ESS_cert_mac.p12', 'windows': 'ESS_cert_win.pfx', 'linux': ''}
        self.certificate_file_path = os.path.join(self.certificates_dir_path, self.certificate_file_name[self.os_name])
        #
        self.cryspy_path = cryspy.__path__[0]
        self.shiboken2_path = shiboken2.__path__[0]
        self.pyside2_path = PySide2.__path__[0]

    def setOsName(self):
        if sys.platform.startswith('darwin'):
            return 'osx'
        elif sys.platform.startswith('lin'):
            return 'linux'
        elif sys.platform.startswith('win'):
            return 'windows'
        else:
            return ''

    #def setReleaseVersion(self):
        # Settings file
        #settings_file_path = os.path.join(project_dir_path, 'App', 'QmlImports', 'easyDiffraction', 'Settings.qml')
        # Find application version
        #release_version = ''
        #with open(settings_file_path, 'r') as f:
            #file_content = f.read()
            #release_version = re.findall('\d+.\d+.\d+', file_content)[0]
            #print("Release version: '{0}'".format(release_version))

class VarsLog:
    def __init__(self):
        self.var = VarsConfig()
        self.qtifw = InstallerFrameworkConfig(self.var.os_name, self.var.scripts_dir_path, self.var.user_home_dir)

    def info(self):
        print('\n***** Variables')
        print()
        print('os_name:           ', self.var.os_name)
        print('organization_name: ', self.var.organization_name)
        print('project_name:      ', self.var.project_name)
        print('installer_name:    ', self.var.installer_name)
        print()
        print('user_home_dir:            ', self.var.user_home_dir)
        print('project_dir_path:         ', self.var.project_dir_path)
        print('scripts_dir_path:         ', self.var.scripts_dir_path)
        print('examples_dir_path:        ', self.var.examples_dir_path)
        print('dist_dir_path:            ', self.var.dist_dir_path)
        print('freezed_app_path:         ', self.var.freezed_app_path)
        print()
        print('qtifw_version:                  ', self.qtifw.version)
        print('qtifw_url:                      ', self.qtifw.url)
        print('qtifw_setup_as_downloaded_path: ', self.qtifw.setup_as_downloaded_path)
        print('qtifw_setup_exe_path:           ', self.qtifw.setup_exe_path[self.var.os_name])
        print('qtifw_binarycreator_path:       ', self.qtifw.binarycreator_path)
        print('qtifw_installerbase_path:       ', self.qtifw.installerbase_path)
        print()
        print('silent_install_script_path: ', self.var.silent_install_script_path)
        print('installer_config_dir_path:  ', self.var.installer_config_dir_path)
        print('installer_config_xml_path:  ', self.var.installer_config_xml_path)
        print('installer_packages_dir_path:', self.var.installer_packages_dir_path)
        print('installer_data_dir_path:    ', self.var.installer_data_dir_path)
        print('installer_dir_path:         ', self.var.installer_dir_path)
        print('installer_exe_name:         ', self.var.installer_exe_name)
        print('installer_exe_path:         ', self.var.installer_exe_path)
        print()
        print('cryspy_path:   ', self.var.cryspy_path)
        print('shiboken2_path:', self.var.shiboken2_path)
        print('pyside2_path:  ', self.var.pyside2_path)
        print()
        print('certificates_zip_path:', self.var.certificates_zip_path)
        print('certificate_file_path:', self.var.certificate_file_path)
        print()
        print('os_specific_separator:   ', self.var.os_specific_separator[self.var.os_name])
        print('os_specific_icon_ext:    ', self.var.os_specific_icon_ext[self.var.os_name])
        print('os_specific_missing_libs:', self.var.os_specific_missing_libs[self.var.os_name])

# Windows
  # lib not found: shiboken2.abi3.dll dependency of c:\python37\lib\site-packages\PySide2\QtGui.pyd, etc.
  # lib not found: MSVCP140.dll dependency of c:\python37\lib\site-packages\PySide2\libGLESv2.dll, etc.
  # lib not found: api-ms-win-core-winrt-string-l1-1-0.dll dependency of c:\python37\lib\site-packages\PySide2\qt5bluetooth.dll
  # lib not found: api-ms-win-core-winrt-l1-1-0.dll dependency of c:\python37\lib\site-packages\PySide2\qt5bluetooth.dll
# macOS
  # Can not find path ./libshiboken2.abi3.5.13.dylib (needed by /Users/travis/.python-venv/lib/python3.6/site-packages/PySide2/QtCore.abi3.so)
