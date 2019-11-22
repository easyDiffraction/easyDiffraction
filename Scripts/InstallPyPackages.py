#!/usr/bin/env python3

import sys
import pip
import Project

def install(*packages):
    Project.printTitle('Install Python packages with PIP')
    for package in packages:
        Project.run('pip', 'install', package)
        print("+ Succeeded to install '{0}'".format(package))

def printSysPath():
    Project.printTitle('Print sys path')
    for path in sys.path:
        if path: print(path)

# Example
if __name__ == '__main__':
    config = Project.Config()

    #printSysPath()

    install(
        'cryspy==0.1.13',
        'PySide2==5.13.1',
        'pyinstaller==3.5',
        'requests==2.22.0',
        'uritemplate==3.0.0',
        'pyyaml==5.1.2',
        'pytest==5.3.0',
        'pytest_mock==1.12.1',
        'pytest-cov==2.8.1',
        'pytest-qt==3.2.2',
        'codecov==2.0.15',
        )
