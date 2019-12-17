#!/usr/bin/env python3

import os, sys
import ast
import zipfile
import Project
import BasicFunctions

if __name__ == "__main__":
    BasicFunctions.printTitle('Sign code')

    config = Project.Config()

    os_name = config['os']['name']
    app_name = config['app']['name']
    app_url = config['app']['url']
    installer_exe_path = config['app']['installer']['exe_path']
    certificates_dir_path = config['project']['subdirs']['certificates']['path']
    certificate_file_path = config['certificate']['path']
    certificates_zip_path = config['certificate']['zip_path']

    if os_name == 'linux':
        print('* No code signing needed for linux')
        exit()

    passwords_dict = ast.literal_eval(sys.argv[1]) if len(sys.argv) > 1 else {'osx':'', 'windows':'', 'zip':''}
    certificate_password = passwords_dict[os_name].replace('\\', '')
    zip_password = passwords_dict['zip']

    print('* Unzip certificates')
    with zipfile.ZipFile(certificates_zip_path) as zf:
        zf.extractall(
            path = certificates_dir_path,
            pwd = bytes(zip_password, 'utf-8')
            )

    if os_name == 'windows':
        print('* Code signing for windows')

        signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x86', 'signtool.exe')

        print('* Import certificate')
        BasicFunctions.run(
            'certutil.exe',
            #'-user',                               # "Current User" Personal store.
            '-p', certificate_password,             # the password for the .pfx file
            '-importpfx', certificate_file_path # name of the .pfx file
            )

        print('* Sign code with imported certificate')
        BasicFunctions.run(
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
        print('* Code signing for osx')

        keychain_name = 'codesign.keychain'
        keychain_password = 'password'
        identity = 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)'

        print('* Create keychain')
        BasicFunctions.run(
            'security', 'create-keychain',
            '-p', keychain_password,
            keychain_name
            )

        print('* Set it to be default keychain')
        BasicFunctions.run(
            'security', 'default-keychain',
            '-s', keychain_name
            )

        print('* List keychains')
        BasicFunctions.run(
            'security', 'list-keychains'
            )

        print('* Unlock created keychain')
        BasicFunctions.run(
            'security', 'unlock-keychain',
            '-p', keychain_password,
            keychain_name
            )

        print('* Import certificate to created keychain')
        BasicFunctions.run(
            'security', 'import',
            certificate_file_path,
            '-k', keychain_name,
            '-P', certificate_password,
            '-T', '/usr/bin/codesign'
            )

        print('* Show certificates')
        BasicFunctions.run(
            'security', 'find-identity',
            '-v'
            )

        print('* Allow codesign to access certificate key from keychain')
        BasicFunctions.run(
            'security', 'set-key-partition-list',
            '-S', 'apple-tool:,apple:,codesign:',
            '-s',
            '-k', keychain_password
            )

        print('* Sign code with imported certificate')
        BasicFunctions.run(
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
