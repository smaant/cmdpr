#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from subprocess import Popen
from tempfile import NamedTemporaryFile
import re
import logging

from github import GitHub, GitHubException
from git import Git, GitException


TOKEN_ENV_KEY = 'CMDPR_TOKEN'

logger = logging.getLogger(__name__)


def pull_request():
    parser = argparse.ArgumentParser(description='Creates GitHub pull request for current branch in current git repo')
    parser.add_argument('-m', '--message', dest='message', type=str, nargs=1, metavar='SUMMARY',
                        help='Pull request summary')
    parser.add_argument('-b', '--base', dest='base', type=str, nargs=1, metavar='BASE_BRANCH', default=['master'],
                        help='Base for pull request, master by default')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Enable debug output')

    args = parser.parse_args()

    if args.debug:
        logging.disable(logging.NOTSET)

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

        base = args.base[0]
        title, body = None, None
        if args.message is None:
            title, body = create_request_title(git.get_commits(base))
        else:
            title = args.message[0]

        if title is None:
            print('ERROR: There\'s no title for pull request')
            return 1

        pr_url = github.create_pull_request(git.get_repo_info(), title, base, body)
        print(pr_url)
    except GitHubException as ex:
        print('ERROR: ' + ex.message)
        return 1


def create_request_title(commits):
    tmpfile = NamedTemporaryFile(mode='w+t', suffix='.txt')
    editor = os.getenv('EDITOR', 'open')

    if len(commits) == 1:
        tmpfile.file.write(commits[0])

    tmpfile.file.write('\n\n# Write title for the pull request. '
                       'First line will be considered as a title, the rest as a body.\n')
    tmpfile.file.write('# All comments and empty lines will be removed. List of commits:\n')
    tmpfile.file.writelines(['# {}\n'.format(x) for x in commits])

    tmpfile.file.close()
    Popen([editor, tmpfile.name]).wait()
    return extract_title_and_body(open(tmpfile.name).read())


def extract_title_and_body(text):
    match = re.findall(r'^([^#\n].*)$', text, re.MULTILINE)
    stripped = [s for s in map(lambda x: x.strip(), match) if s != '']
    title = stripped[0] if len(stripped) > 0 else None
    body = '\n'.join(stripped[1:]) if len(stripped) > 1 else None
    return title, body