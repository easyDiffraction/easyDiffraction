#!/usr/bin/env python3

import os, sys
import ast
import zipfile
import Project

if __name__ == "__main__":
    config = Project.Config()

    os_name = config['os']['name']
    app_name = config['app']['name']
    app_url = config['app']['url']
    installer_exe_path = config['app']['installer']['exe_path']
    certificates_dir_path = config['project']['subdirs']['certificates']['path']
    certificate_file_path = config['certificate']['path']
    certificates_zip_path = config['certificate']['zip_path']

    passwords_dict = ast.literal_eval(sys.argv[1]) if len(sys.argv) > 1 else {'osx':'', 'windows':'', 'zip':''}
    certificate_password = passwords_dict[os_name].replace('\\', '')
    zip_password = passwords_dict['zip']

    Project.printTitle('Unzip certificates')
    with zipfile.ZipFile(certificates_zip_path) as zf:
        zf.extractall(
            path = certificates_dir_path,
            pwd = bytes(zip_password, 'utf-8')
            )

    Project.printTitle('Sign code')
    if os_name == 'linux':
        exit()

    elif os_name == 'windows':
        signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x86', 'signtool.exe')

        Project.printTitle('Import certificate')
        Project.run(
            'certutil.exe',
            #'-user',                               # "Current User" Personal store.
            '-p', certificate_password,             # the password for the .pfx file
            '-importpfx', certificate_file_path # name of the .pfx file
            )

        Project.printTitle('Sign code with imported certificate')
        Project.run(
            signtool_exe_path, 'sign',              # info - https://msdn.microsoft.com/en-us/data/ff551778(v=vs.71)
            #'/f', certificate_file_path,           # signing certificate in a file
            #'/p', certificate_password,            # password to use when opening a PFX file
            '/sm',                                  # use a machine certificate store instead of a user certificate store
            '/d', app_name,                         # description of the signed content
            '/du', app_url,                         # URL for the expanded description of the signed content
            '/t', 'http://timestamp.digicert.com',  # URL to a timestamp server
            '/debug',
            '/v',                                   # display the verbose version of operation and warning messages
            installer_exe_path
            )

    elif os_name == 'osx':
        keychain_name = 'codesign.keychain'
        keychain_password = 'password'
        identity = 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)'

        Project.printTitle('Create keychain')
        Project.run(
            'security', 'create-keychain',
            '-p', keychain_password,
            keychain_name
            )

        Project.printTitle('Set it to be default keychain')
        Project.run(
            'security', 'default-keychain',
            '-s', keychain_name
            )

        Project.printTitle('List keychains')
        Project.run(
            'security', 'list-keychains'
            )

        Project.printTitle('Unlock created keychain')
        Project.run(
            'security', 'unlock-keychain',
            '-p', keychain_password,
            keychain_name
            )

        Project.printTitle('Import certificate to created keychain')
        Project.run(
            'security', 'import',
            certificate_file_path,
            '-k', keychain_name,
            '-P', certificate_password,
            '-T', '/usr/bin/codesign'
            )

        Project.printTitle('Show certificates')
        Project.run(
            'security', 'find-identity',
            '-v'
            )

        Project.printTitle('Allow codesign to access certificate key from keychain')
        Project.run(
            'security', 'set-key-partition-list',
            '-S', 'apple-tool:,apple:,codesign:',
            '-s',
            '-k', keychain_password
            )

        Project.printTitle('Sign code with imported certificate')
        Project.run(
            'codesign',
            '--deep',
            '--force',
            '--verbose',
            # --timestamp URL
            '--sign', identity,
            installer_exe_path
            )



# INFO
# https://gist.github.com/curiousstranger/309035
# https://apple.stackexchange.com/questions/242795/command-line-keychain-access-not-showing-any-results
# https://stackoverflow.com/questions/39868578/security-codesign-in-sierra-keychain-ignores-access-control-settings-and-ui-p
# security create-keychain -p 'password' build.keychain # security delete-keychain build.keychain
# security default-keychain -s build.keychain # security default-keychain -s login.keychain
# security list-keychains
# security unlock-keychain -p 'password' build.keychain
# security import Certificates/ESS_cert_mac.p12 -k build.keychain -P '<certificate_password>' -T /usr/bin/codesign
# security find-identity -v
# security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k 'password'
# codesign --deep --force --verbose --sign 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)' dist/easyDiffractionInstaller.app
