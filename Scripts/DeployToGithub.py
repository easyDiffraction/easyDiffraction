#!/usr/bin/env python3

import os, sys
#import re
import requests
import shutil
import yaml # pip install pyyaml
from uritemplate import URITemplate # pip install uritemplate
import BasicFunctions
import Project

# CLASSES

class GithubAgent: # Agent, Communicator, Connector?
    def __init__(self, owner, repo, token):
        self._owner = owner
        self._repo = repo
        self._token = token
        self._repo_url = 'https://api.github.com/repos/{0}/{1}'.format(self._owner, self._repo)
        self._auth_header = {'Authorization': 'Token {0}'.format(self._token)}
        self._upload_zip_header = {**self._auth_header, 'Content-Type': 'application/zip'}
        self._checkUrlAccessible(self._repo_url)
        # branches
        self._branches_url = '{0}/branches'.format(self._repo_url)
        self._checkUrlAccessible(self._branches_url)
        self._selected_branch_name = None
        # releases
        self._releases_url = '{0}/releases'.format(self._repo_url)
        self._checkUrlAccessible(self._releases_url)
        self._releases_list = self._requestReleases(self._releases_url)
        self._selected_release_tag_name = None
        self._selected_release_id = None
        self._selected_release_upload_url = None
        # assets
        self._assets_url = '{0}/assets'.format(self._releases_url)
        self._selected_release_assets_url = None
        self._selected_release_assets_dict = {}
        #self._asset_file_name = None

    def _printRequestStatus(self, response):
        print("* Status code: '{0}'".format(response.status_code))
        print("* Status info: '{0}'".format(response.text))

    def _checkUrlAccessible(self, url):
        response = requests.get(url, headers=self._auth_header)
        if response:
            print("* Succeeded to access '{0}'".format(url))
        else:
            print("- Failed to access '{0}'".format(url))
            self._printRequestStatus(response)
            sys.exit()

    # Get list of all the releases (including draft ones)
    def _requestReleases(self, url):
        response = requests.get(url, headers=self._auth_header)
        if response:
            print("+ Succeeded to get list of releases from '{0}'".format(url))
            return response.json()
        else:
            print("- Failed to get list of releases from '{0}'".format(url))
            self._printRequestStatus(response)
            return []

    # Check if branch already exists
    def _branchExistByName(self, name):
        branch_url = '{0}/{1}'.format(self._branches_url, name)
        response = requests.get(branch_url, headers=self._auth_header)
        if response:
            print("+ Succeeded to find branch '{0}'".format(name))
            return True
        else:
            print("- Failed to find branch '{0}'".format(name))
            self._printRequestStatus(response)
            return False

    def selectBranchByName(self, name):
        if not self._branchExistByName(name):
            sys.exit()
        self._selected_branch_name = name

    # Check if release already exists
    def releaseExistByTagName(self, tag_name):
        for release in self._releases_list:
            if release.get('tag_name') == tag_name:
                print("+ Succeeded to find release '{0}' in previously downloaded list".format(tag_name))
                return True
        print("- Failed to find release '{0}' in previously downloaded list".format(tag_name))
        return False

    def selectReleaseByTagName(self, tag_name):
        # Update list of releases if needed
        if not self.releaseExistByTagName(tag_name):
            self._releases_list = self._requestReleases(self._releases_url)
        # Exit, if release is still not found
        if not self.releaseExistByTagName(tag_name):
            sys.exit()
        self._selected_release_tag_name = tag_name
        # Get id and upload_url of the desired release
        for release in self._releases_list:
            if release['tag_name'] == tag_name:
                self._selected_release_id = release['id']
                self._selected_release_upload_url = release['upload_url']
                break

    def uploadAsset(self, asset_dir, installer_exe_name, app_name, os_name, tag_name):
        # Define asset file/path
        asset_file_name = '{0}_{1}'.format(app_name, os_name)
        if tag_name is not None:
            asset_file_name += '_{0}'.format(tag_name)
        asset_file_path_without_ext = os.path.join(asset_dir, asset_file_name)
        asset_file_format = 'zip'
        asset_file_name += '.{0}'.format(asset_file_format)
        asset_file_path = os.path.join(asset_dir, asset_file_name)
        # Make MakeArchive
        input_name = installer_exe_name
        input_dir = asset_dir
        output_format = asset_file_format
        output_path = asset_file_path_without_ext
        shutil.make_archive(output_path, output_format, input_dir, input_name)
        if os.path.isfile(asset_file_path):
            print("+ Succeeded to find local asset file '{0}'".format(asset_file_path))
        else:
            print("- Failed to find local asset file '{0}'".format(asset_file_path))
            sys.exit()
        # Get list of assets for the desired release
        self._selected_release_assets_url = '{0}/{1}/assets'.format(self._releases_url, self._selected_release_id)
        response = requests.get(self._selected_release_assets_url, headers=self._auth_header)
        if response:
            print("+ Succeeded to find remote assets for release '{0}'".format(self._selected_release_tag_name))
            self._selected_release_assets_dict = response.json()
        else:
            print("- Failed to find remote assets for release '{0}'".format(self._selected_release_tag_name))
        # Delete existing asset (if any)
        for asset in self._selected_release_assets_dict:
            if asset['name'] == asset_file_name:
                print("+ Succeeded to find remote asset '{0}'".format(asset_file_name))
                asset_url = '{0}/{1}'.format(self._assets_url, asset['id'])
                response = requests.delete(asset_url, headers=self._auth_header)
                if response:
                    print("+ Succeeded to delete remote asset '{0}'".format(asset_file_name))
                else:
                    print("- Failed to delete remote asset '{0}'".format(asset_file_name))
                    self._printRequestStatus(response)
                    sys.exit()
        # Upload asset
        asset_upload_url = URITemplate(self._selected_release_upload_url).expand(name=asset_file_name)
        response = requests.post(asset_upload_url, headers=self._upload_zip_header, data=open(asset_file_path, 'rb').read())
        if response:
            print("+ Succeeded to upload local asset file '{0}'".format(asset_file_name))
        else:
            print("- Failed to upload local asset file '{0}'".format(asset_file_name))
            self._printRequestStatus(response)
            sys.exit()

    def createRelease(self, config):
        release_name = config['name']
        response = requests.post(self._releases_url, headers=self._auth_header, json=config)
        if response:
            print("+ Succeeded to create release '{0}'".format(release_name))
        else:
            print("- Failed to create release '{0}'".format(release_name))
            self._printRequestStatus(response)
            sys.exit()

# RELEASE CONFIG

class ReleaseConfig:
    def __init__(self, version, branch, date, changes):
        self._draft = True
        self._prerelease = self._isPrerelease(version)
        self._tag_name = self._releaseTagName(version=version, branch=branch)
        self._name = self._releaseName(version=version, branch=branch, date=date)
        self._body = self._releaseBody(version=version, branch=branch, changes=changes)
        self._target_commitish = self._targetCommitish(version=version, branch=branch)

    # try https://codereview.stackexchange.com/questions/124688/regex-to-extract-version-info
    def _isPrerelease(self, version):
        major = int(version.split('.')[0])
        if major == 0:
            return True
        return False

    def _isMaster(self, branch):
        if branch == 'master':
            return True
        return False

    def _isFinal(self, version, branch):
        if branch == 'v{0}'.format(version): #re.search('v\d+\.\d+\.\d+', branch)
            return True
        return False

    def _releaseTagName(self, version, branch):
        if self._isMaster(branch) or self._isFinal(version=version, branch=branch):
            return 'v{0}'.format(version)
        return branch

    def _releaseName(self, version, branch, date):
        if self._isMaster(branch) or self._isFinal(version=version, branch=branch):
            return 'Version {0} ({1})'.format(version, date)
        return branch

    def _releaseBody(self, version, branch, changes):
        if self._isMaster(branch) or self._isFinal(version=version, branch=branch):
            body = ''
            for item in changes:
                body += '* {0}{1}'.format(item, os.linesep)
            return body
        return ''

    def _targetCommitish(self, version, branch):
        if self._isMaster(branch) or self._isFinal(version=version, branch=branch):
            return 'master'
        return branch

    def json(self):
        return {
            "tag_name": self._tag_name,
            "target_commitish": self._target_commitish,
            "name": self._name,
            "body": self._body,
            "draft": self._draft,
            "prerelease": self._prerelease
            }

# MAIN

if __name__ == "__main__":
    BasicFunctions.printTitle('Deploy to GitHub releases')

    # Exit if pull request
    pull_request = BasicFunctions.environmentVariable('TRAVIS_PULL_REQUEST')
    if pull_request != 'false':
        print("* Deployment not needed. It's a pull request No. '{}'".format(pull_request))
        exit()

    # Load config
    config = Project.Config()

    # Init github communication
    owner = config.getVal('github', 'owner')
    repo = config.getVal('github', 'repo')
    token = BasicFunctions.environmentVariable('GITHUB_TOKEN')
    #token = BasicFunctions.environmentVariable('GITHUB_TOKEN', default='...')
    github = GithubAgent(owner=owner, repo=repo, token=token)

    # Create release config
    version = config.getVal('release', 'version')
    date = config.getVal('release', 'date')
    changes = config.getVal('release', 'changes')
    branch = BasicFunctions.environmentVariable('TRAVIS_BRANCH')
    #branch = BasicFunctions.environmentVariable('TRAVIS_BRANCH', default='upload-artifacts')
    release = ReleaseConfig(version=version, branch=branch, date=date, changes=changes)

    # Select desired branch
    target_commitish = release.json()['target_commitish']
    github.selectBranchByName(target_commitish)

    # Select desired release (create release, if it doesn't exist yet)
    tag_name = release.json()['tag_name']
    if not github.releaseExistByTagName(tag_name):
        github.createRelease(release.json())
    github.selectReleaseByTagName(tag_name)

    # Upload asset
    if tag_name != 'master':
        app_name = config.getVal('app', 'name')
        os_name = config.getVal('os', 'name')
        asset_dir = config.getVal('project', 'subdirs', 'distribution', 'path')
        installer_exe_name = config.getVal('app', 'installer', 'exe_name')
        github.uploadAsset(asset_dir=asset_dir, installer_exe_name=installer_exe_name, app_name=app_name, os_name=os_name, tag_name=tag_name)
