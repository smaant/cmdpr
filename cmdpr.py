#!/usr/bin/env python
# coding: utf-8
import os
import sys
import argparse

from cmdpr.github import GitHub, GitHubException
from cmdpr import git

TOKEN_ENV_KEY = 'CMDPR_TOKEN'


def abort(message, error_code):
    print('ERROR: ' + message)
    sys.exit(error_code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates GitHub pull request for current branch in current git repo')
    parser.add_argument('-m', '--message', dest='message', type=str, nargs=1, metavar='SUMMARY', required=True,
                        help='Pull request summary')
    parser.add_argument('-b', '--base', dest='base', type=str, nargs=1, metavar='BASE_BRANCH', default=['master'],
                        help='Base for pull request, master by default')

    args = parser.parse_args()

    token = os.environ.get(TOKEN_ENV_KEY)
    if token is None:
        abort('Add GitHub token to environment variable ' + TOKEN_ENV_KEY, 1)

    if not git.is_git_repo():
        abort('Your current directory is not a git repository', 2)

    if not git.is_github_repo():
        abort('Your current git repository is not a GitHub repository', 3)

    github = GitHub(token)
    if not github.is_token_valid():
        abort('GitHub token is invalid or revoked', 4)

    branch = git.get_current_branch()
    try:
        pr_url = github.create_pull_request(branch, args.message[0], args.base[0])
        print(pr_url)
    except GitHubException as ex:
        abort(ex.message, 5)
