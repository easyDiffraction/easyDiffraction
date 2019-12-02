#!/usr/bin/env python3

import os
import Project
import Functions

def pyFilePaths(input_dir_path):
    parent_dir_path = os.path.dirname(input_dir_path)
    file_paths = []
    for (dir_path, dir_names, file_names) in os.walk(input_dir_path):
        for file_name in file_names:
            _, file_ext = os.path.splitext(file_name)
            if file_ext == '.py':
                file_path = os.path.join(dir_path, file_name)
                relative_path = os.path.relpath(file_path, parent_dir_path)
                file_paths.append(relative_path)
    return file_paths

def environmentVariable(name, default=None):
    value = os.getenv(name)
    if value is not None:
        return value
    else:
        print("- Failed to find environment variable '{0}', using default value '{1}'".format(name, default))
        return default

if __name__ == "__main__":
    Functions.printTitle('Report Complexity')

    config = Project.Config()
    project_dir_path = config['project']['dir_path']
    app_dir_path = config['project']['subdirs']['app']['path']
    file_paths = pyFilePaths(app_dir_path)
    #branch = environmentVariable('TRAVIS_BRANCH')

    Functions.runAsIs(
        'wily',
        'build',                                                            # By default, it will assume the directory is a git repository and will scan back through 50 revisions
        app_dir_path,                                                       # directory to be scanned
        '--max-revisions', '1',                                             # -n, --max-revisions <max_revisions>: The maximum number of historical commits to archive
        )
    Functions.runAsIs(
        'wily',
        'diff',                                                             # compare the last cached revision of the code with the current metrics (for the current environment).
        *file_paths,                                                        # to see the changes in metrics for a list of files
        '--changes-only',                                                   # --all, --changes-only: Show all files, instead of changes only
        '--no-detail',                                                      # --detail, --no-detail: Show function/class level metrics where available
        '--metrics', 'maintainability.mi,cyclomatic.complexity,raw.loc',    # --metrics <metrics>: comma-seperated list of metrics, see list-metrics for choices
        )
