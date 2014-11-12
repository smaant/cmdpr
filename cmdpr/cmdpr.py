#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from subprocess import Popen
from tempfile import NamedTemporaryFile
import re

from github import GitHub, GitHubException
from git import Git, GitException


TOKEN_ENV_KEY = 'CMDPR_TOKEN'


def pull_request():
    parser = argparse.ArgumentParser(description='Creates GitHub pull request for current branch in current git repo')
    parser.add_argument('-m', '--message', dest='message', type=str, nargs=1, metavar='SUMMARY', required=True,
                        help='Pull request summary')
    parser.add_argument('-b', '--base', dest='base', type=str, nargs=1, metavar='BASE_BRANCH', default=['master'],
                        help='Base for pull request, master by default')

    args = parser.parse_args()

    token = os.environ.get(TOKEN_ENV_KEY)
    if token is None:
        print('ERROR: Add GitHub token to environment variable ' + TOKEN_ENV_KEY)
        return 1

    try:
        git = Git()
    except GitException as ex:
        print('ERROR: ' + ex.message)
        return 1

    try:
        github = GitHub(token)
        pr_url = github.create_pull_request(git.get_repo_info(), args.message[0], args.base[0])
        print(pr_url)
    except GitHubException as ex:
        print('ERROR: ' + ex.message)
        return 1


def create_request_title(commits):
    tmpfile = NamedTemporaryFile(mode='w+t', suffix='.txt')
    editor = os.getenv('EDITOR', 'open')

    if len(commits) == 1:
        tmpfile.file.write(commits[0])
    else:
        tmpfile.file.write('\n\n# Write title for the pull request. '
                           'First line will be considered as a title, the rest as a body.\n')
        tmpfile.file.write('# All comments and empty lines will be removed. List of commits:\n')
        tmpfile.file.writelines(['# {}\n'.format(x) for x in commits])

    tmpfile.file.close()
    Popen([editor, tmpfile.name]).wait()
    return extract_title_and_body(open(tmpfile.name).read())


def extract_title_and_body(text):
    match = re.findall(r'^([^#\n].*)$', text, re.MULTILINE)


create_request_title(Git().get_commits('master'))