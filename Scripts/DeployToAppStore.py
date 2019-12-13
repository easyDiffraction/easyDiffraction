#!/usr/bin/env python3

import os, sys
import Project
import BasicFunctions

# FUNCTIONS

def createSnapcraftDir(dir_name):
    message = "create snapcraft dir '{}'".format(dir_name)
    try:
        BasicFunctions.run('mkdir', dir_name)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def decryptCertificates():
    message = "decrypt certificates"
    try:
        BasicFunctions.run(
            'openssl', 'aes-256-cbc',
            '-K', BasicFunctions.environmentVariable('encrypted_d23b8f89b93f_key'), #'$encrypted_d23b8f89b93f_key',
            '-iv', BasicFunctions.environmentVariable('encrypted_d23b8f89b93f_iv'), #'$encrypted_d23b8f89b93f_iv',
            '-in', 'Certificates/snapCredentials.tar.enc',
            '-out', 'Certificates/snapCredentials.tar',
            '-d'
            )
        #command = 'openssl aes-256-cbc -K $encrypted_d23b8f89b93f_key -iv $encrypted_d23b8f89b93f_iv -in Certificates/snapCredentials.tar.enc -out Certificates/snapCredentials.tar -d'
        #os.system(command)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def extractCertificates():
    message = "extract certificates"
    try:
        BasicFunctions.run(
            'tar',
            'xvf', 'Certificates/snapCredentials.tar',
            '-C', 'Certificates'
            )
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def moveCertificates(dir_name):
    message = "move certificates to '{}'".format(dir_name)
    try:
        BasicFunctions.run('mv', 'Certificates/snapCredentialsEdge', dir_name+'/snapcraft.cfg')
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

# docker run -v $(pwd):/easyDiffraction -t cibuilds/snapcraft:core18 sh -c "apt update -qq && cd /easyDiffraction && snapcraft && snapcraft push *.snap --release edge"


def osDependentDeploy():
    config = Project.Config()
    os_name = config['os']['name']
    if os_name == 'linux':
        snapcraft_dir_name = '.snapcraft'
        createSnapcraftDir(snapcraft_dir_name)
        decryptCertificates()
        extractCertificates()
        moveCertificates(snapcraft_dir_name)
    else:
        message = "* No deployment for '{}' App Store is implemented".format(os_name)
        print(message)

# MAIN

if __name__ == "__main__":
    BasicFunctions.printTitle('Deploy to App Store')
    osDependentDeploy()
