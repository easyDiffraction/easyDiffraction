#!/usr/bin/env python3

import os, sys
import shutil
import requests
import subprocess
import BasicFunctions

# FUNCTIONS

def downloadFile(url, destination):
    message = "download from '{0}'".format(url)
    try:
        file = requests.get(url, allow_redirects=True)
        open(destination, 'wb').write(file.content)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def attachDmg(file):
    message = "attach '{0}'".format(file)
    try:
        BasicFunctions.run('hdiutil', 'attach', file)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def setEnvVariable(name, value):
    message = "set environment variable '{0}' to '{1}'".format(name, value)
    try:
        os.environ[name] = value
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def addReadPermission(file):
    message = "add read permissions to '{0}'".format(file)
    try:
        BasicFunctions.run('chmod', 'a+x', file)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def createFile(path, content):
    message = "create file '{0}'".format(path)
    try:
        dir = os.path.dirname(path)
        os.makedirs(dir, exist_ok=True)
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def createDir(path):
    message = "create dir '{0}'".format(path)
    try:
        os.mkdir(path)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def copyFile(source, destination):
    message = "copy file to '{0}'".format(source, os.path.join(os.path.basename(source), destination))
    try:
        shutil.copy2(source, destination, follow_symlinks=True)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def moveDir(source, destination):
    message = "move dir to '{0}'".format(source, os.path.join(os.path.basename(source), destination))
    try:
        shutil.move(source, destination)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

def installSilently(installer, silent_script):
    message = "install '{0}'".format(installer)
    try:
        BasicFunctions.run(
            installer,
            '--script', silent_script,
            '--no-force-installations'
            )
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)
