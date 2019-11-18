#!/usr/bin/env python3

import os, sys
import re
import ast
import subprocess
import zipfile
import requests
from uritemplate import URITemplate
import Variables

################
# GET PARAMETERS
################

# Global constants
var = Variables.VarsConfig()

# BRANCH NAME
os.environ['TRAVIS_BRANCH'] = 'upload-artifacts'
branch_name = os.environ['TRAVIS_BRANCH']
if branch_name != '':
    print("Branch name: '{0}'".format(branch_name))
else:
    print("Failed to get branch name.")
    exit()

# RELEASE INFO

# Project
project_name = 'easyDiffraction'

# Main paths
scripts_dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir_path = os.path.realpath(os.path.join(scripts_dir_path, '..'))

# Settings file
settings_file_path = os.path.join(project_dir_path, 'App', 'QmlImports', 'easyDiffraction', 'Settings.qml')

# Find application version
release_version = ''
with open(settings_file_path, 'r') as f:
    file_content = f.read()
    release_version = re.findall('\d+.\d+.\d+', file_content)[0]
    print("Release version: '{0}'".format(release_version))

# RELEASE TAG
release_tag = ''
if re.search('v\d+\.\d+\.\d+', branch_name): # if release with tag of 'v1.0.12' format
    release_tag = 'v{0}'.format(release_version)
else:
    release_tag = '{0}-v{1}'.format(branch_name, release_version)
print("Release tag: '{0}'".format(release_tag))

# RELEASE NAME
release_name = 'easydiffraction-' + release_tag
print("Release name: '{0}'".format(release_name))

# ACCESS TOKEN
access_token = os.environ['GITHUB_TOKEN']

# FILE TO UPLOAD
upload_file_name = '{0}_{1}_v{2}.zip'.format(var.project_name, var.os_name, release_version)
upload_file_path = os.path.join(var.installer_dir_path, upload_file_name)
print("Upload file name: '{0}'".format(upload_file_name))
print("Upload file path: '{0}'".format(upload_file_path))

##################
# UPLOAD ARTIFACTS
##################

owner = 'easydiffraction'
repo = 'easydiffraction'
authorization_info = {'Authorization': 'Token {0}'.format(access_token)}
api_base_url = 'https://api.github.com/repos/{0}/{1}'.format(owner, repo)
content_type_info = {'Content-Type': 'application/zip'}

# Get list of all the releases (including draft ones)
releases_url = '{0}/releases'.format(api_base_url)
response = requests.get(releases_url, headers=authorization_info)
releases_list = response.json()
if response:
    print("Succeeded to get list of all releases for '{0}'".format(api_base_url))
else:
    print("Failed to get list of all releases for '{0}'".format(api_base_url))
    exit()

# Get both id and upload_url of the specific release
release_id = ''
release_upload_url = ''
for release in releases_list:
    if release['tag_name'] == release_tag:
        release_id = release['id']
        release_upload_url = release['upload_url']
        print("Succeeded to get release_id and release_upload_url.")
        ###print("release_id: {0}".format(release_id))
        ###print("release_upload_url: {0}".format(release_upload_url))
        break
    else:
        print("Failed to get release_id and release_upload_url.")
        exit()

# Get list of assets for the specific release
release_assets_url = '{0}/releases/{1}/assets'.format(api_base_url, release_id)
response=requests.get(release_assets_url, headers=authorization_info)
release_assets_dict = response.json()
if response:
    print("Succeeded to get list of assets")
else:
    print("Failed to get list of assets for release")
    exit()

# Delete existing asset (if any) and show info message
for asset in release_assets_dict:
    if asset['name'] == upload_file_name:
        print("File '{0}' already exists, deleting.".format(upload_file_name))
        asset_url = '{0}/releases/assets/{1}'.format(api_base_url, asset['id'])
        response = requests.delete(asset_url, headers=authorization_info)
        if response:
            print("Succeeded to delete asset '{0}'".format(upload_file_name))
        else:
            print("Failed to delete asset '{0}'".format(upload_file_name))
            exit()

# Upload asset and show info message
asset_upload_url = URITemplate(release_upload_url).expand(name=upload_file_name) # rename file to be uploaded, if needed
print("asset_upload_url '{0}'".format(asset_upload_url))

response = requests.post(asset_upload_url, headers={**authorization_info, **content_type_info}, data=open(upload_file_path, 'rb').read()) # use local file
if response:
    print("File '{0}' is successfully uploaded.".format(upload_file_name))
else:
    print("Failed to upload '{0}' file.".format(upload_file_name))
    exit()

# Check
#https://github.com/smarie/python-mini-lambda/blob/master/ci_tools/github_release.py
