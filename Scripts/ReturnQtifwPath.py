#!/usr/bin/env python3

import sys
import Project

if __name__ == '__main__':
    config = Project.Config()
    path = config['qtifw']['dir_path']
    sys.stdout.write(path)
    sys.stdout.flush()
    sys.exit(0)
