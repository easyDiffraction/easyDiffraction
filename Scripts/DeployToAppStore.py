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

def saveDockerImage(docker_image, downloaded_image_path):
    message = "save docker image '{}'".format(docker_image)
    if os.path.exists(downloaded_image_path):
        message = "* Docker image '{0}' for snapcraft is already downloaded to '{1}'".format(docker_image, downloaded_image_path)
        print(message)
        return()
    try:
        os.system('docker pull {}'.format(docker_image))
        os.system('docker save {0} | gzip > {1}'.format(docker_image, downloaded_image_path))
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def loadDockerImage(downloaded_image_path):
    message = "load docker image from '{}'".format(downloaded_image_path)
    try:
        #os.system('docker load < .soft/snap.tar.gz')
        os.system('gzip -dc {} | docker load'.format(downloaded_image_path))
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def runDockerImage(docker_image, project_dir_path, branch):
    message = "push release 'edge' for branch '{}'".format(branch)
    try:
        BasicFunctions.run(
            'docker', 'run',
            '--volume', '{}:/easyDiffraction'.format(project_dir_path), # Bind mount a volume
            '--tty', # Allocate a pseudo-TTY
            docker_image,
            'sh', '-c', "apt update -qq && cd /easyDiffraction && snapcraft && snapcraft push *.snap --release edge"
            )
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def osDependentDeploy():
    config = Project.Config()
    os_name = config['os']['name']
    project_dir_path = config['project']['dir_path']
    branch = BasicFunctions.environmentVariable('TRAVIS_BRANCH')
    if os_name == 'linux':
        if branch == 'develop':
            snapcraft_dir_name = '.snapcraft'
            docker_image = 'cibuilds/snapcraft:core18'
            downloaded_image_path = '.soft/snap.tar.gz'
            createSnapcraftDir(snapcraft_dir_name)
            decryptCertificates()
            extractCertificates()
            moveCertificates(snapcraft_dir_name)
            saveDockerImage(docker_image, downloaded_image_path)
            loadDockerImage(downloaded_image_path)
            runDockerImage(docker_image, project_dir_path, branch)
        else:
            message = "* No deployment for branch '{}' is implemented".format(branch)
            print(message)
    else:
        message = "* No deployment for '{}' App Store is implemented".format(os_name)
        print(message)

# MAIN

if __name__ == "__main__":
    BasicFunctions.printTitle('Deploy to App Store')

    # Exit if pull request
    pull_request = BasicFunctions.environmentVariable('TRAVIS_PULL_REQUEST')
    if pull_request != 'false':
        print("* Deployment not needed. It's a pull request No. '{}'".format(pull_request))
        exit()

    # Deploy 
    osDependentDeploy()
