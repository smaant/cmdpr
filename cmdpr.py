#!/usr/bin/env python
# coding: utf-8
import os
import sys

from cmdpr.github import GitHub, GitHubException
from cmdpr import git


TOKEN_ENV_KEY = 'CMDPR_TOKEN'

token = os.environ.get(TOKEN_ENV_KEY)
if token is None:
    print 'ERROR: Add GitHub token to environment variable ' + TOKEN_ENV_KEY
    sys.exit(1)

github = GitHub(token)
if not github.is_token_valid():
    print 'ERROR: GitHub token is invalid or revoked'
    sys.exit(2)

branch = git.get_current_branch()
try:
    pr_url = github.create_pull_request(branch, "Super duper PR")
    print pr_url
except GitHubException as ex:
    print 'ERROR: ' + ex.message
    exit(3)
