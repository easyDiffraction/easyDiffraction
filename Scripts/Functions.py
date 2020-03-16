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

def dict2xml(d, root_node=None, add_xml_version=True):
    wrap          = False if root_node is None or isinstance(d, list) else True
    root          = 'root' if root_node is None else root_node
    root_singular = root[:-1] if root[-1] == 's' else root
    xml           = ''
    attr          = ''
    children      = []

    if add_xml_version:
        xml += '<?xml version="1.0" ?>'

    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, (dict, list)):
                children.append(dict2xml(value, root=key, add_xml_version=False))
            elif key[0] == '@':
                attr = attr + ' ' + key[1::] + '="' + str(value) + '"'
            else:
                xml = '<' + key + ">" + str(value) + '</' + key + '>'
                children.append(xml)

    elif isinstance(d, list):
        for value in d:
            children.append(dict2xml(value, root=root_singular, add_xml_version=False))

    else:
        raise TypeError(f"Type {type(d)} is not supported")

    end_tag = '>' if children else '/>'

    if wrap:
        xml = '<' + root + attr + end_tag

    if children:
        xml += "".join(children)

        if wrap:
            xml += '</' + root + '>'

    return xml
