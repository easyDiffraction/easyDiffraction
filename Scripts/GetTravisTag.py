#!/usr/bin/env python3

import re
import os
import sys

release_number = sys.argv[1] if len(sys.argv) > 2 else '0.0.1'
branch = sys.argv[2] if len(sys.argv) > 2 else 'master'

if re.search('v\d+\.\d+\.\d+', branch): # if release with tag of 'v1.0.12' format
    travis_tag = 'v{0}'.format(release_number)
else:
    travis_tag = '{0}-v{1}'.format(branch, release_number)

print("TRAVIS_BRANCH: ", os.environ['TRAVIS_BRANCH'])
print(travis_tag)
