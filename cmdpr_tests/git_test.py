# coding: utf-8
import os
import json
from unittest import TestCase

from cmdpr.git import Git
from cmdpr import get_root_path
from cmdpr_tests import get_resource_path, get_resources_path


class GitTestCase(TestCase):

    def setUp(self):
        os.chdir(get_root_path())
        self.git = Git()

    def test_not_github_repo(self):
        dir_name = os.path.join(get_resources_path(), 'not-github-repo')
        os.chdir(dir_name)
        self.assertTrue(self.git.is_git_repo())
        self.assertFalse(self.git.is_github_repo())

    def test_github_repo(self):
        self.assertTrue(self.git.is_git_repo())
        self.assertTrue(self.git.is_github_repo())

    def test_not_git_repo(self):
        not_git_dir = os.path.dirname(get_root_path())
        os.chdir(not_git_dir)
        self.assertFalse(self.git.is_git_repo())
        self.assertFalse(self.git.is_github_repo())

    def test_get_current_branch(self):
        dir_name = os.path.join(get_resources_path(), 'not-github-repo')
        os.chdir(dir_name)
        self.assertEqual(self.git.get_current_branch(), 'master')

    def test_get_repo_info(self):
        data = json.load(open(get_resource_path('repoinfo.json')))
        for case in data:
            self.assertEqual(self.git._parse_remote_info(case['input']), case['expected'])

    def test_get_repo_owner(self):
        repo_info = self.git.get_repo_info()
        self.assertEqual(repo_info['owner'], 'smaant')
        self.assertEqual(repo_info['name'], 'cmdpr')
        self.assertEqual(repo_info['remote'], 'origin')
        self.assertIsNotNone(repo_info['branch'])
