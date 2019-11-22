#!/usr/bin/env python3

import os, sys
import subprocess

# FUNCTIONS

def printTitle(title):
    #print('{0}***** {1}'.format(os.linesep, title))
    print('***** {0}'.format(title))

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
