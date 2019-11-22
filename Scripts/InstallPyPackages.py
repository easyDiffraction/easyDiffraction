#!/usr/bin/env python3

import sys
import Functions

# FUNCTIONS

def printSysPath():
    for path in sys.path:
        if path: print(path)

def upgradePip():
    Functions.run('python', '-m', 'pip', 'install', '--upgrade', 'pip')
    print("+ Succeeded to upgrade PIP")

def install(*packages):
    for package in packages:
        Functions.run('pip', 'install', package)
        print("+ Succeeded to install '{0}'".format(package))

# MAIN

if __name__ == '__main__':
    #Functions.printTitle('Print sys path')
    #printSysPath()
    Functions.printTitle('Upgrade PIP and install packages')
    upgradePip()
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
