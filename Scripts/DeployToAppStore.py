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
            '-K', BasicFunctions.environmentVariable('encrypted_d23b8f89b93f_key'),
            '-iv', BasicFunctions.environmentVariable('encrypted_d23b8f89b93f_iv'),
            '-in', 'Certificates/snapCredentials.tar.enc',
            '-out', 'Certificates/snapCredentials.tar',
            '-d'
            )
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

def saveDockerImage():
    message = "save docker image '{}'".format('')
    if os.path.exists('.soft/snap.tar.gz'):
        message = "* Docker image for snapcraft is already downloaded {}".format('')
        print(message)
        return()
    try:
        os.system('ls .soft')
        os.system('docker save cibuilds/snapcraft:core18 | gzip > .soft/snap.tar.gz')
        os.system('ls .soft')
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def loadDockerImage():
    message = "load docker image '{}'".format('')
    BasicFunctions.runAsIs('docker', 'image', 'ls')
    BasicFunctions.runAsIs('docker', 'images')
    BasicFunctions.runAsIs('docker', 'container', 'ls')
    try:
        os.system('docker image ls')
        os.system('docker load < .soft/snap.tar.gz')
        os.system('docker image ls')
        BasicFunctions.runAsIs('docker', 'container', 'ls')
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)
        BasicFunctions.runAsIs('docker', 'image', 'ls')
        BasicFunctions.runAsIs('docker', 'images')
        BasicFunctions.runAsIs('docker', 'container', 'ls')

def runDockerImage(project_dir_path, branch):
    message = "push release 'edge' for branch '{}'".format(branch)
    BasicFunctions.runAsIs('docker', 'image', 'ls')
    BasicFunctions.runAsIs('docker', 'images')
    BasicFunctions.runAsIs('docker', 'container', 'ls')
    try:
        BasicFunctions.runAsIs('docker', 'run', 'cibuilds/snapcraft:core18')
        #BasicFunctions.run(
        #    'docker', 'run',
            #'--volume', '{}:/easyDiffraction'.format(project_dir_path), # Bind mount a volume
            #'--tty', # Allocate a pseudo-TTY
        #    'cibuilds/snapcraft:core18',
            #'sh', '-c', "apt update -qq && cd /easyDiffraction && snapcraft && snapcraft push *.snap --release edge"
        #    )
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)
        BasicFunctions.runAsIs('docker', 'container', 'ls')

def osDependentDeploy():
    config = Project.Config()
    os_name = config['os']['name']
    project_dir_path = config['project']['dir_path']
    branch = BasicFunctions.environmentVariable('TRAVIS_BRANCH')
    if os_name == 'linux':
        if branch == 'develop':
            snapcraft_dir_name = '.snapcraft'
            createSnapcraftDir(snapcraft_dir_name)
            decryptCertificates()
            extractCertificates()
            moveCertificates(snapcraft_dir_name)
            saveDockerImage()
            loadDockerImage()
            runDockerImage(project_dir_path, branch)
        else:
            message = "* No deployment for branch '{}' is implemented".format(branch)
            print(message)
    else:
        message = "* No deployment for '{}' App Store is implemented".format(os_name)
        print(message)

# MAIN

if __name__ == "__main__":
    BasicFunctions.printTitle('Deploy to App Store')
    osDependentDeploy()
