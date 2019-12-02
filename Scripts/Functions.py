#!/usr/bin/env python3

import os, sys
import subprocess

# FUNCTIONS

def colorTitle(title):
    return '\033[0;30;43m' + title + '\033[0m' # http://ozzmaker.com/add-colour-to-text-in-python/

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
    print(colorTitle(empty_title))
    print(colorTitle(title))
    print(colorTitle(empty_title))

def run(*args, report_success=False, report_errors=True, exit_on_error=True):
    result = subprocess.run(
        args,
        #capture_output=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,    # converts the output to a string instead of a byte array.
        #check=True                  # forces the Python method to throw an exception if the underlying process encounters errors
    )
    if report_success and result.stdout:
        print("+ Success:{0}{1}".format(os.linesep, result.stdout))
    if report_errors and result.stderr:
        print("- Fail:{0}{1}".format(os.linesep, result.stderr))
        if exit_on_error:
            sys.exit()

if __name__ == "__main__":
    print('before')
    printTitle('Test title')
    print('after')
