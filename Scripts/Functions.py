#!/usr/bin/env python3

import os, sys
import shutil
import requests
import subprocess

# FUNCTIONS

def coloredText(message='', style='1', background_color='49m', text_color='39'):
    # http://ozzmaker.com/add-colour-to-text-in-python/
    escape_code = '\033['
    reset = '0m'
    return "{0}{1};{2};{3}{4}{0}{5}".format(escape_code, style, text_color, background_color, message, reset)

def coloredTitle(title):
    black = '30'
    yellow = '43m'
    return coloredText(message=title, style='0', background_color=yellow, text_color=black)

def printTitle(title):
    #print('{0}***** {1}'.format(os.linesep, title))
    max_len = 80
    fill_len = max_len - len(title)
    if (fill_len % 2) == 0:
        left_fill_len = int(fill_len / 2)
        right_fill_len = left_fill_len
    else:
        left_fill_len = int((fill_len + 1) / 2)
        right_fill_len = left_fill_len - 1
    title = (' '*left_fill_len) + title + (' '*right_fill_len)
    #title = title.upper()
    empty_title = ' '*max_len
    print()
    print(coloredTitle(empty_title))
    print(coloredTitle(title))
    print(coloredTitle(empty_title))

def runAsIs(*args):
    result = subprocess.run(
        args,
        capture_output=False,
        universal_newlines=True,    # converts the output to a string instead of a byte array.
        #check=True                  # forces the Python method to throw an exception if the underlying process encounters errors
    )

def run(*args, report_success=False, report_errors=True, exit_on_error=True):
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,    # converts the output to a string instead of a byte array.
        #check=True                  # forces the Python method to throw an exception if the underlying process encounters errors
    )
    if report_success and result.stdout:
        print("+ Success:{0}{1}".format(os.linesep, result.stdout))
    if report_errors and result.stderr:
        print("- Fail:{0}{1}".format(os.linesep, result.stderr))
    if exit_on_error and result.stderr:
        sys.exit()

def printFailMessage(message, exception=None):
    bright_red = '31'
    extended_message = "- Failed to {}".format(message)
    if exception:
        extended_message += os.linesep
        extended_message += str(exception)
    report = coloredText(message=extended_message, text_color=bright_red)
    print(report)

def printSuccessMessage(message):
    bright_green = '32'
    extended_message = "+ Succeeded to {}".format(message)
    report = coloredText(message=extended_message, text_color=bright_green)
    print(report)

def downloadFile(url, destination):
    message = "download from '{0}'".format(url)
    try:
        file = requests.get(url, allow_redirects=True)
        open(destination, 'wb').write(file.content)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def attachDmg(file):
    message = "attach '{0}'".format(file)
    try:
        run('hdiutil', 'attach', file)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def setEnvVariable(name, value):
    message = "set environment variable '{0}' to '{1}'".format(name, value)
    try:
        os.environ[name] = value
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def addReadPermission(file):
    message = "add read permissions to '{0}'".format(file)
    try:
        run('chmod', 'a+x', file)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def createFile(path, content):
    message = "create file '{0}'".format(path)
    try:
        dir = os.path.dirname(path)
        os.makedirs(dir, exist_ok=True)
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def createDir(path):
    message = "create dir '{0}'".format(path)
    try:
        os.mkdir(path)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def copyFile(source, destination):
    message = "copy file to '{0}'".format(source, os.path.join(os.path.basename(source), destination))
    try:
        shutil.copy2(source, destination, follow_symlinks=True)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def moveDir(source, destination):
    message = "move dir to '{0}'".format(source, os.path.join(os.path.basename(source), destination))
    try:
        shutil.move(source, destination)
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

def installSilently(installer, silent_script):
    message = "install '{0}'".format(installer)
    try:
        run(
            installer,
            '--script', silent_script,
            '--no-force-installations'
            )
    except Exception as exception:
        printFailMessage(message, exception)
        sys.exit()
    else:
        printSuccessMessage(message)

if __name__ == "__main__":
    printTitle('Functions')
