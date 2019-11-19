#!/usr/bin/env python3

import os, sys
import re
import ast
import subprocess
import zipfile
import requests
from uritemplate import URITemplate
import yaml     # pip3 install pyyaml
import Variables

# Read config
config_file_path = os.path.join(os.getcwd(), 'Configs', 'Project.yml')
with open(config_file_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Get list of all the releases (including draft ones)
response = requests.get(config['github']['releases_url'], headers=config['github']['auth_header'])
releases_list = response.json()
if response:
    print("Succeeded to get list of all releases for '{0}'".format(config['github']['releases_url']))
else:
    print("Failed to get list of all releases for '{0}'".format(config['github']['releases_url']))
    print("Status code: '{0}'".format(response.status_code))
    print("Status info: '{0}'".format(response.text))
    sys.exit()

# Get id of the specific release, if release is already exist
release_exist = False
for release in releases_list:
    if release['tag_name'] == config['ci']['branch']:
        release_exist = True
        break

# Create release, if it doesn't exist yet
#https://developer.github.com/v3/repos/releases/#create-a-release
#https://stackoverflow.com/questions/5207269/how-to-release-a-build-artifact-asset-on-github-with-a-script
if release_exist:
    print("Release '{0}' already exists".format(config['ci']['branch'])) # release_tag
else:
    print("Release '{0}' doesn't exist, creating".format(config['ci']['branch'])) # release_tag
    release_description = {
      "tag_name": config['release']['tag'],
      "target_commitish": config['ci']['branch'], # need to check if branch exists
      "name": config['release']['name'],
      "body": config['release']['description'],
      "draft": config['release']['draft'],
      "prerelease": config['release']['prerelease']
    }
    response = requests.post(config['github']['releases_url'], headers=config['github']['upload_zip_header'], json=release_description)
    if response:
        print("Release '{0}' is successfully created".format(release_description['name']))
    else:
        print("Failed to create release '{0}'".format(release_description['name']))
        print("Status code: '{0}'".format(response.status_code))
        print("Status info: '{0}'".format(response.text))
        sys.exit()

    # Reread list list of all the releases (including draft ones)
    response = requests.get(config['github']['releases_url'], headers=config['github']['auth_header'])
    releases_list = response.json()
    if response:
        print("Succeeded to get list of all releases for '{0}'".format(config['github']['api_base_url']))
    else:
        print("Failed to get list of all releases for '{0}'".format(config['github']['api_base_url']))
        print("Status code: '{0}'".format(response.status_code))
        print("Status info: '{0}'".format(response.text))
        sys.exit()

# Get id and upload_url of the specific release, if release is already exist
release_id = ''
release_upload_url = ''
for release in releases_list:
    if release['tag_name'] == config['ci']['branch']:
        release_id = release['id']
        release_upload_url = release['upload_url']
        break

# Get list of assets for the specific release
release_assets_url = '{0}/releases/{1}/assets'.format(config['github']['api_base_url'], release_id)
print('release_assets_url', release_assets_url)
response=requests.get(release_assets_url, headers=config['github']['auth_header'])
release_assets_dict = response.json()
if response:
    print("Succeeded to get list of assets")
else:
    print("No assets are found")

# Delete existing asset (if any) and show info message
for asset in release_assets_dict:
    if asset['name'] == config['release']['file_name']:
        print("File '{0}' already exists, deleting.".format(config['release']['file_name']))
        asset_url = '{0}/releases/assets/{1}'.format(config['github']['api_base_url'], asset['id'])
        response = requests.delete(asset_url, headers=config['github']['auth_header'])
        if response:
            print("Succeeded to delete asset '{0}'".format(config['release']['file_name']))
        else:
            print("Failed to delete asset '{0}'".format(config['release']['file_name']))
            print("Status code: '{0}'".format(response.status_code))
            print("Status info: '{0}'".format(response.text))
            sys.exit()

# Upload asset and show info message
asset_upload_url = URITemplate(release_upload_url).expand(name=config['release']['file_name']) # rename file to be uploaded, if needed
response = requests.post(asset_upload_url, headers=config['github']['upload_zip_header'], data=open(config['release']['file_path'], 'rb').read()) # use local file
if response:
    print("File '{0}' is successfully uploaded.".format(config['release']['file_name']))
else:
    print("Failed to upload '{0}' file.".format(config['release']['file_name']))
    print("Status code: '{0}'".format(response.status_code))
    print("Status info: '{0}'".format(response.text))
    sys.exit()

# Check
#https://github.com/smarie/python-mini-lambda/blob/master/ci_tools/github_release.py
#https://docs.travis-ci.com/user/deployment/pages/#setting-the-github-token
#https://developer.github.com/v3/repos/

# Pre-commit: Referencing current branch in github readme.md
#https://stackoverflow.com/questions/18673694/referencing-current-branch-in-github-readme-md/35368808#35368808
