# coding: utf-8
from subprocess import Popen, PIPE
import re


class Git:

    def __init__(self):
        if not self.is_git_repo():
            raise GitException('Your current directory is not a git repository')

        if not self.is_github_repo():
            raise GitException('Your current git repository is not a GitHub repository')

    def _run(self, args):
        process = Popen(args, stdout=PIPE, stderr=PIPE)
        return process.communicate()[0]

    def is_git_repo(self):
        return Popen(['git', 'status'], stdout=PIPE, stderr=PIPE).wait() == 0

    def is_github_repo(self):
        output = self._run(['git', 'remote', '-v'])
        match = re.findall(r'(?:(?:git@)|(?:https://))github.com.*\(push\)$', output, re.MULTILINE)
        return len(match) == 1

    def get_current_branch(self):
        output = self._run(['git', 'branch'])
        match = re.findall(r'^\* (.*)$', output, re.MULTILINE)
        if len(match) == 1:
            return match[0]
        else:
            raise RuntimeError('Exactly one element expected, was <{}>'.format(match))

    def _parse_remote_info(self, remote_output):
        """
        :param remote_output: output of `git remote -v`
        """
        match = re.search(r'^([^\s]+).*github.com:([^/]+)/(.+).git\s\(push\)$', remote_output, re.MULTILINE)
        if match is None:
            raise RuntimeError('Unable to parse response of \'git remote -v\':\n' + remote_output)
        else:
            return {
                'remote': match.group(1),
                'owner': match.group(2),
                'name': match.group(3)
            }

    def get_repo_info(self):
        remote_output = self._run(['git', 'remote', '-v'])
        repo_info = self._parse_remote_info(remote_output)
        repo_info['branch'] = self.get_current_branch()
        return repo_info

    def get_commits(self, base):
        remote = self.get_repo_info()['remote']
        branch = self.get_current_branch()
        output = self._run(['git', 'log',
                            '{remote}/{base}..{remote}/{branch}'.format(remote=remote, base=base, branch=branch),
                            '--pretty=%s'])
        return output.splitlines()


class GitException(Exception):
    def __init__(self, message):
        super(GitException, self).__init__(message)