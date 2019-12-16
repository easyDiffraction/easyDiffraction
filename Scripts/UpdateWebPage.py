#!/usr/bin/env python3

import os, sys
#import re
import requests
import shutil
import yaml # pip install pyyaml
from uritemplate import URITemplate # pip install uritemplate
import Project
import BasicFunctions

import re
import base64

# CLASSES

class GithubAgent: # Agent, Communicator, Connector?
    def __init__(self, owner, repo, token):
        # repo
        self._owner = owner
        self._repo = repo
        self._token = token
        self._auth_header = {'Authorization': 'Token {0}'.format(self._token)}
        # get file
        self._file_name = 'index.html'
        self._file_url = 'https://api.github.com/repos/{0}/{1}/contents/{2}'.format(self._owner, self._repo, self._file_name)
        self._file_dict = self._requestFile(self._file_url)
        self._original_file_sha = self._file_dict['sha']
        self._original_file_content = self._base64ToString(self._file_dict['content'])
        # update file
        self._updated_file_content = self._updateVersionAndDate(self._original_file_content)
        # upload new version
        self._uploadUpdatedFile(self._stringToBase64AsString(self._updated_file_content), self._original_file_sha)

    def _printRequestStatus(self, response):
        print("* Status code: '{0}'".format(response.status_code))
        print("* Status info: '{0}'".format(response.text))

    def _base64ToString(self, b):
        return base64.b64decode(b).decode('utf-8')

    def _stringToBase64(self, s):
        return base64.b64encode(s.encode('utf-8'))

    def _stringToBase64AsString(self, s):
        return self._stringToBase64(s).decode('utf-8')

    def _requestFile(self, url):
        response = requests.get(url, headers=self._auth_header)
        if response:
            print("+ Succeeded to get file from '{0}'".format(url))
            return response.json()
        else:
            print("- Failed to get file from '{0}'".format(url))
            self._printRequestStatus(response)
            return []

    def _updateVersionAndDate(self, content):
        config = Project.Config()
        version = config.getVal('release', 'version')
        date = config.getVal('release', 'date')
        out = re.sub(r'Version&nbsp;\d+\.\d+\.\d+ \(\d{1,2} \w{3} \d{4}\)', 'Version&nbsp;{0} ({1})'.format(version, date), content)
        out = re.sub(r'v\d+\.\d+\.\d+', 'v{0}'.format(version), out)
        return out

    def _uploadUpdatedFile(self, content, sha):
        config = {
            'message': 'Bumped release links [ci skip]',
            #'committer': {
            #    'name': 'Travis CI',
            #    'email': 'travis@travis-ci.org'
            #}),
            'branch': 'master',
            'content': content,
            'sha': sha
        }
        response = requests.put(self._file_url, json=config, headers=self._auth_header)
        if response:
            print("+ Succeeded to upload updated page to '{0}'".format(self._file_url))
        else:
            print("- Failed to upload updated page to '{0}'".format(self._file_url))
            self._printRequestStatus(response)
            sys.exit()

# LOCAL FUNCS

def environmentVariable(name, default=None):
    value = os.getenv(name)
    if value is not None:
        return value
    else:
        print("- Failed to find environment variable '{0}', using default value '{1}'".format(name, default))
        return default

# MAIN

if __name__ == "__main__":
    BasicFunctions.printTitle('Update web page')

    config = Project.Config()
    version = config.getVal('release', 'version')
    branch = environmentVariable('TRAVIS_BRANCH')

    if branch == 'v{0}'.format(version): #re.search('v\d+\.\d+\.\d+', branch)
        owner = 'easyDiffraction'
        repo = 'easyDiffraction.github.io'
        token = environmentVariable('GITHUB_TOKEN')
        #token = environmentVariable('GITHUB_TOKEN', default='...')
        github = GithubAgent(owner=owner, repo=repo, token=token)
    else:
        message = "* No update needed for branch '{}'".format(branch)
        print(message)
