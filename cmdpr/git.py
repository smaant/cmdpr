# coding: utf-8
from subprocess import Popen, PIPE
import re


def _run(args):
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    return process.communicate()[0]


def get_current_branch():
    output = _run(['git', 'branch'])
    match = re.findall(r'^\* (.*)$', output, re.MULTILINE)
    if len(match) == 1:
        return match[0]
    else:
        raise RuntimeError('Exactly one element expected, was <{}>'.format(match))


def is_git_repo():
    return Popen(['git', 'status'], stdout=PIPE, stderr=PIPE).wait() == 0


def is_github_repo():
    output = _run(['git', 'remote', '-v'])
    match = re.findall(r'(?:(?:git@)|(?:https://))github.com.*\(push\)$', output, re.MULTILINE)
    return len(match) == 1


def get_repo_owner():
    output = _run(['git', 'remote', '-v'])
    match = re.findall(r'github.com:([^/]+)/.*\(push\)$', output, re.MULTILINE)
    if len(match) != 1:
        raise RuntimeError('Exactly one match expected, was <{}>'.format(match))
    else:
        return match[0]


def get_repo_name():
    output = _run(['git', 'remote', '-v'])
    match = re.findall(r'github.com:.*/([^.]+).*\(push\)$', output, re.MULTILINE)
    if len(match) != 1:
        raise RuntimeError('Exactly one match expected, was <{}>'.format(match))
    else:
        return match[0]
