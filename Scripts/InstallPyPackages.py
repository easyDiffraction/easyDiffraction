#!/usr/bin/env python3

import sys
import BasicFunctions


# FUNCTIONS

def printSysPath():
    for path in sys.path:
        if path:
            print(path)


def upgradePip():
    message = "upgrade PIP"
    try:
        BasicFunctions.run('python', '-m', 'pip', 'install', '--upgrade', 'pip')
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def installFromGitE(owner, repo, branch, egg):
    url = "git://github.com/{0}/{1}.git@{2}#egg={3}".format(owner, repo, branch, egg)
    message = "install from '{}'".format(url)
    try:
        BasicFunctions.run('pip', 'install', '-e', url, exit_on_error=False)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        # sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def installFromGit(owner, repo, branch):
    url = "https://github.com/{0}/{1}/archive/{2}.zip".format(owner, repo, branch)
    message = "install from '{}'".format(url)
    try:
        BasicFunctions.run('pip', 'install', url)
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)


def install(*packages):
    for package in packages:
        message = "install '{}'".format(package)
        try:
            BasicFunctions.run('pip', 'install', package)
        except Exception as exception:
            BasicFunctions.printFailMessage(message, exception)
            sys.exit()
        else:
            BasicFunctions.printSuccessMessage(message)


# MAIN

if __name__ == '__main__':
    BasicFunctions.printTitle('Upgrade PIP and install packages')

    upgradePip()

    installFromGit(owner='ikibalin', repo='cryspy', branch='transition-to-version-0.2')

    install(
        #'cryspy==0.1.13',
        'scipy==1.4.1',
        'numpy==1.18.1',
        'easyInterface>=0.0.6',
        'PySide2==5.13.1',
        'pyinstaller==3.5',  # develop version - https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
        'requests==2.22.0',
        'uritemplate==3.0.0',
        'pyyaml==5.1.2',
        'dicttoxml==1.7.4',
        'asteval==0.9.18',
        'pytest==5.3.0',
        'pytest_mock==1.12.1',
        'pytest-cov==2.8.1',
        'pytest-qt==3.2.2',
        'wily==1.13.0',
        'codecov==2.0.15',
        'dicttoxml',
    )

    if BasicFunctions.osName() == 'windows':
        install('pypiwin32')
