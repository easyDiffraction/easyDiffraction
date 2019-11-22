#!/usr/bin/env python3

import os, sys
import subprocess

# FUNCTIONS

def printTitle(title):
    #print('{0}***** {1}'.format(os.linesep, title))
    max_len = 80
    spaces_len = 1
    fill_len = max_len - 2*spaces_len - len(title)
    if (fill_len % 2) == 0:
        left_fill_len = int(fill_len / 2)
        right_fill_len = left_fill_len
    else:
        left_fill_len = int((fill_len + 1) / 2)
        right_fill_len = left_fill_len - 1
    s = title.upper()
    s = ('*'*left_fill_len) + (' '*spaces_len) + s + (' '*spaces_len) + ('*'*right_fill_len)
    #s = '\033[0;37;44m' + s + '\033[0m' # http://ozzmaker.com/add-colour-to-text-in-python/
    s = '\033[0;30;43m' + s + '\033[0m' # http://ozzmaker.com/add-colour-to-text-in-python/
    s = os.linesep + s
    print(s)

def run(*args):
    result = subprocess.run(
        args,
        #capture_output=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,    # converts the output to a string instead of a byte array.
        #check=True                  # forces the Python method to throw an exception if the underlying process encounters errors
    )
    #if result.stdout:
    #    print("+ Success:{0}{1}".format(os.linesep, result.stdout))
    if result.stderr:
        print("- Fail:{0}{1}".format(os.linesep, result.stderr))
        sys.exit()

if __name__ == "__main__":
    print('before')
    printTitle('Test title')
    print('after')
