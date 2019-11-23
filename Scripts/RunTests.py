#
# script for running unit tests for easyDiffraction
#
# run with
# > python runTests.py
#

import sys
import os
import pytest
import warnings
import Functions

sys.path.append('App')
sys.path.append(os.path.join('App','PyImports'))
sys.path.append('.')

Functions.printTitle('Run unit tests')

# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# automatically discover and run all tests under ./Tests
# files with names starting with `test_` are considered valid test files

args = ['--cov=App', 'Tests']

# add potential arguments like -k or -m
if len(sys.argv) > 1:
    args += sys.argv[1:]
print(args)

errno = pytest.main(args)
sys.exit(errno)
