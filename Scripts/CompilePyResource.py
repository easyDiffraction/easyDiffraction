#!/usr/bin/env python3

import os, sys
import Project
import BasicFunctions

def createExamplesResource():
    message = "create examples resource file"
    try:
        config = Project.Config()
        project_dir_path = config['project']['dir_path']
        BasicFunctions.run(
            'pyside2-rcc',
            '{0}/App/Examples.qrc'.format(project_dir_path),
            '-o', '{0}/App/Examples.py'.format(project_dir_path),       # Write output to file rather than stdout
            '-no-compress'                                              # Disable all compression
            )
    except Exception as exception:
        BasicFunctions.printFailMessage(message, exception)
        sys.exit()
    else:
        BasicFunctions.printSuccessMessage(message)

if __name__ == "__main__":
    BasicFunctions.printTitle('Compile qt resource file (.qrc) into python resource file (.py)')
    createExamplesResource()
