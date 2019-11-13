#
# script for running unit tests for easyDiffraction
#
# run with
# > python runTests.py
#

import sys
import os
import pytest

sys.path.append('App')
sys.path.append(os.path.join('App','PyImports'))
sys.path.append('.')

# automatically discover and run all tests under ./Tests
# files with names starting with `test_` are considered valid test files

args = ['--cov=App', 'Tests']

# add potential arguments like -k or -m
if len(sys.argv) > 1:
    args += sys.argv[1:]
print (args)
pytest.main(args)

