#!/usr/bin/env python3

import os, sys
import yaml     # pip3 install pyyaml
import re

def absolutePath(relative_path):
    current_working_dir = os.getcwd()
    absolute_path = os.path.join(current_working_dir, relative_path)
    return absolute_path

def getConfig(config_relative_file_path):
    config_file_path = absolutePath(config_relative_file_path)
    if not os.path.isfile(config_file_path):
        print("File '{0}' doesn't exist".format(config_file_path))
        return {}
    with open(config_file_path, 'r') as file:
        file_content = yaml.load(file, Loader=yaml.FullLoader)
        return file_content

def osName():
    platform = sys.platform
    if platform.startswith('darwin'):
        return 'osx'
    elif platform.startswith('lin'):
        return 'linux'
    elif platform.startswith('win'):
        return 'windows'
    else:
        print("Unsupported platform '{0}'".format(platform))
        return None

def environmentVariable(name, default=None):
    value = os.getenv(name)
    if value is not None:
        return value
    else:
        print("Failed to find environment variable '{0}'".format(name))
        print("Use default value '{0}'".format(default))
        return default

def isPrerelease(version):
    # try https://codereview.stackexchange.com/questions/124688/regex-to-extract-version-info
    major = int(version.split('.')[0])
    if major == 0:
        return True
    return False

def isDraftRelease(branch):
    # not draft if branch name is of 'v1.0.12' format
    if config['ci']['branch'] == 'master': #re.search('v\d+\.\d+\.\d+', branch):
        return False
    return True

def releaseName(config):
    if config['release']['draft']:
        return config['ci']['branch']
    return 'Version {0} ({1})'.format(config['release']['version'], config['release']['date'])

def releaseTag(config):
    if config['release']['draft']:
        return config['ci']['branch']
    return 'v{0}'.format(config['release']['version'])

def releaseDescription(config):
    description = ''
    for item in config['release']['changes']:
        description += '* {0}{1}'.format(item, os.linesep)
    return description

def printAsYaml(py_dict):
    yml = yaml.dump(py_dict, sort_keys=False, indent=2, allow_unicode=True)
    print(yml)

def writeProjectConfig(py_dict, file_path):
    with open(file_path, 'w') as out_file:
        yaml.dump(py_dict, out_file, sort_keys=False, indent=2, allow_unicode=True)

# MAIN

# public parameters
config = getConfig(os.path.join('Configs', 'Template.yml'))

config['structure']['distribution'] = absolutePath(config['structure']['distribution'])
config['structure']['installer'] = absolutePath(config['structure']['distribution'])
config['structure']['configs'] = absolutePath(config['structure']['configs'])
config['structure']['scripts'] = absolutePath(config['structure']['scripts'])
config['structure']['certificates'] = absolutePath(config['structure']['certificates'])
config['structure']['examples'] = absolutePath(config['structure']['examples'])

config['github']['api_base_url'] = 'https://api.github.com/repos/{0}/{1}'.format(config['github']['owner'], config['github']['repo'])
config['github']['releases_url'] = '{0}/releases'.format(config['github']['api_base_url'])

config['ci']['os'] = osName()
config['ci']['branch'] = environmentVariable('TRAVIS_BRANCH', default='upload-artifacts') # upload-artifacts

config['release']['draft'] = isDraftRelease(config['ci']['branch'])
config['release']['prerelease'] = isPrerelease(config['release']['version'])
config['release']['tag'] = releaseTag(config)
config['release']['name'] = releaseName(config)
config['release']['description'] = releaseDescription(config)
config['release']['file_name'] = '{0}_{1}_{2}.zip'.format(config['app']['name'], config['ci']['os'], config['release']['tag'])
config['release']['file_path'] = os.path.join(config['structure']['installer'], config['release']['file_name'])

# print config
printAsYaml(config)

# private parameters
auth = getConfig(os.path.join('Configs', 'Auth.yml'))

config['github']['token'] = environmentVariable('GITHUB_TOKEN', default=auth.get('github_token'))
config['github']['auth_header'] = {'Authorization': 'Token {0}'.format(config['github']['token'])}
config['github']['upload_zip_header'] = {'Content-Type': 'application/zip', **config['github']['auth_header']}

# save config to file
writeProjectConfig(config, os.path.join(config['structure']['configs'], 'Project.yml'))
