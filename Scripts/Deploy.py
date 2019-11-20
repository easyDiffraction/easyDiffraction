#!/usr/bin/env python3

import os, sys
#import re
import requests
import shutil
import yaml # pip3 install pyyaml
from uritemplate import URITemplate
import Variables

# CLASS

class ProjectConfig:
    def __init__(self, *path_items):
        self._working_dir = os.getcwd()
        self._relative_path = os.path.join(*path_items)
        self._absolute_path = os.path.join(self._working_dir, self._relative_path)
        self._config = self._loadConfig(self._absolute_path)

    def _loadConfig(self, file_path):
        if not os.path.isfile(file_path):
            print("   Failed to find config '{0}'".format(file_path))
            sys.exit()
        with open(file_path, 'r') as file:
            file_content = yaml.load(file, Loader=yaml.FullLoader)
            return file_content

    def osName(self):
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

    def getVal(self, *keys):
        current_level = self._config
        for key in keys:
            if key in current_level:
                current_level = current_level[key]
            else:
                return None
        return current_level

    def toAbsolutePath(self, releative_path):
        return os.path.join(self._working_dir, releative_path)

    def printAsYaml(self):
        yml = yaml.dump(self._config, sort_keys=False, indent=2, allow_unicode=True)
        print(yml)

# CLASS

class GithubAgent: # Agent, Communicator, Connector?
    def __init__(self, owner, repo, token):
        self._owner = owner
        self._repo = repo
        self._token = token
        self._repo_url = 'https://api.github.com/repos/{0}/{1}'.format(self._owner, self._repo)
        self._checkUrlAccessible(self._repo_url)
        self._auth_header = {'Authorization': 'Token {0}'.format(self._token)}
        self._upload_zip_header = {**self._auth_header, 'Content-Type': 'application/zip'}
        # branches
        self._branches_url = '{0}/branches'.format(self._repo_url)
        self._checkUrlAccessible(self._branches_url)
        self._selected_branch_name = None
        # releases
        self._releases_url = '{0}/releases'.format(self._repo_url)
        self._checkUrlAccessible(self._releases_url, headers=self._auth_header)
        self._releases_list = self._requestReleases(self._releases_url, headers=self._auth_header)
        self._selected_release_tag_name = None
        self._selected_release_id = None
        self._selected_release_upload_url = None
        # assets
        self._assets_url = '{0}/assets'.format(self._releases_url)
        self._selected_release_assets_url = None
        self._selected_release_assets_dict = {}
        #self._asset_file_name = None

    def _printRequestStatus(self, response):
        print("Status code: '{0}'".format(response.status_code))
        print("Status info: '{0}'".format(response.text))

    def _checkUrlAccessible(self, url, headers=None):
        response = requests.get(url, headers=headers)
        if response:
            print("Succeeded to access '{0}'".format(url))
        else:
            print("   Failed to access '{0}'".format(url))
            self._printRequestStatus(response)
            sys.exit()

    # Get list of all the releases (including draft ones)
    def _requestReleases(self, url, headers=None):
        response = requests.get(url, headers=headers)
        if response:
            print("Succeeded to get list of releases from '{0}'".format(url))
            return response.json()
        else:
            print("   Failed to get list of releases from '{0}'".format(url))
            self._printRequestStatus(response)
            return []

    # Check if branch already exists
    def _branchExistByName(self, name):
        branch_url = '{0}/{1}'.format(self._branches_url, name)
        response = requests.get(branch_url, headers=self._auth_header)
        if response:
            print("Succeeded to find branch '{0}'".format(name))
            return True
        else:
            print("   Failed to find branch '{0}'".format(name))
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
                print("Succeeded to find release '{0}' in previously downloaded list".format(tag_name))
                return True
        print("   Failed to find release '{0}' in previously downloaded list".format(tag_name))
        return False

    def selectReleaseByTagName(self, tag_name):
        # Update list of releases if needed
        if not self.releaseExistByTagName(tag_name):
            self._releases_list = self._requestReleases(self._releases_url, headers=self._auth_header)
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

    def uploadAsset(self, asset_dir, app_name, os_name, tag_name):
        # Define asset file/path
        asset_file_name = '{0}_{1}'.format(app_name, os_name)
        if tag_name is not None:
            asset_file_name += '_{0}'.format(tag_name)
        asset_file_path_without_ext = os.path.join(asset_dir, asset_file_name)
        asset_file_format = 'zip'
        asset_file_name += '.{0}'.format(asset_file_format)
        asset_file_path = os.path.join(asset_dir, asset_file_name)
        # Make MakeArchive
        var = Variables.VarsConfig()
        input_name = var.installer_exe_name
        input_dir = asset_dir
        output_format = asset_file_format
        output_path = asset_file_path_without_ext
        shutil.make_archive(output_path, output_format, input_dir, input_name)
        if os.path.isfile(asset_file_path):
            print("Succeeded to find local asset file '{0}'".format(asset_file_path))
        else:
            print("   Failed to find local asset file '{0}'".format(asset_file_path))
            sys.exit()
        # Get list of assets for the desired release
        self._selected_release_assets_url = '{0}/{1}/assets'.format(self._releases_url, self._selected_release_id)
        response = requests.get(self._selected_release_assets_url, headers=self._auth_header)
        if response:
            print("Succeeded to find remote assets for release '{0}'".format(self._selected_release_tag_name))
            self._selected_release_assets_dict = response.json()
        else:
            print("   Failed to find remote assets for release '{0}'".format(self._selected_release_tag_name))
        # Delete existing asset (if any)
        for asset in self._selected_release_assets_dict:
            if asset['name'] == asset_file_name:
                print("Succeeded to find remote asset '{0}'".format(asset_file_name))
                asset_url = '{0}/{1}'.format(self._assets_url, asset['id'])
                response = requests.delete(asset_url, headers=self._auth_header)
                if response:
                    print("Succeeded to delete remote asset '{0}'".format(asset_file_name))
                else:
                    print("   Failed to delete remote asset '{0}'".format(asset_file_name))
                    self._printRequestStatus(response)
                    sys.exit()
        # Upload asset
        asset_upload_url = URITemplate(self._selected_release_upload_url).expand(name=asset_file_name)
        response = requests.post(asset_upload_url, headers=self._upload_zip_header, data=open(asset_file_path, 'rb').read())
        if response:
            print("Succeeded to upload local asset file '{0}'".format(asset_file_name))
        else:
            print("   Failed to upload local asset file '{0}'".format(asset_file_name))
            self._printRequestStatus(response)
            sys.exit()

    def createRelease(self, config):
        release_name = config['name']
        response = requests.post(self._releases_url, headers=self._auth_header, json=config)
        if response:
            print("Succeeded to create release '{0}'".format(release_name))
        else:
            print("   Failed to create release '{0}'".format(release_name))
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

    def _isFinal(self, version, branch):
        if branch == 'v{0}'.format(version): #re.search('v\d+\.\d+\.\d+', branch)
            return True
        return False

    def _releaseTagName(self, version, branch):
        if self._isFinal(version=version, branch=branch):
            return 'v{0}'.format(version)
        return branch

    def _releaseName(self, version, branch, date):
        if self._isFinal(version=version, branch=branch):
            return 'Version {0} ({1})'.format(version, date)
        return branch

    def _releaseBody(self, version, branch, changes):
        if self._isFinal(version=version, branch=branch):
            body = ''
            for item in changes:
                body += '* {0}{1}'.format(item, os.linesep)
            return body
        return ''

    def _targetCommitish(self, version, branch):
        if self._isFinal(version=version, branch=branch):
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

# LOCAL FUNCS

def environmentVariable(name, default=None):
    value = os.getenv(name)
    if value is not None:
        return value
    else:
        print("   Failed to find environment variable '{0}', using default value '{1}'".format(name, default))
        return default

# MAIN

if __name__ == "__main__":
    # Read configs
    #auth = ProjectConfig('Configs', 'Auth.yml')
    project = ProjectConfig('Configs', 'Project.yml')

    # Init github communication
    owner = project.getVal('github', 'owner')
    repo = project.getVal('github', 'repo')
    #token = environmentVariable('GITHUB_TOKEN', default=auth.getVal('github_token'))
    token = environmentVariable('GITHUB_TOKEN')
    github = GithubAgent(owner=owner, repo=repo, token=token)

    # Create release config
    version = project.getVal('release', 'version')
    date = project.getVal('release', 'date')
    changes = project.getVal('release', 'changes')
    #branch = environmentVariable('TRAVIS_BRANCH', default='upload-artifacts')
    branch = environmentVariable('TRAVIS_BRANCH')
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
    app_name = project.getVal('app', 'name')
    os_name = project.osName()
    asset_dir = project.toAbsolutePath(project.getVal('structure', 'installer'))
    github.uploadAsset(asset_dir=asset_dir, app_name=app_name, os_name=os_name, tag_name=tag_name)
