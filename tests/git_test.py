# coding: utf-8
import os
from unittest import TestCase

from cmdpr import git
from cmdpr import get_root_path
from tests import get_resources_path


class GitTestCase(TestCase):

    def setUp(self):
        os.chdir(get_root_path())

    def test_not_github_repo(self):
        dir_name = os.path.join(get_resources_path(), 'not-github-repo')
        os.chdir(dir_name)
        self.assertTrue(git.is_git_repo())
        self.assertFalse(git.is_github_repo())

    def test_github_repo(self):
        self.assertTrue(git.is_git_repo())
        self.assertTrue(git.is_github_repo())

    def test_not_git_repo(self):
        not_git_dir = os.path.dirname(get_root_path())
        os.chdir(not_git_dir)
        self.assertFalse(git.is_git_repo())
        self.assertFalse(git.is_github_repo())

    def test_get_current_branch(self):
        dir_name = os.path.join(get_resources_path(), 'not-github-repo')
        os.chdir(dir_name)
        self.assertEqual(git.get_current_branch(), 'master')

    def test_get_repo_owner(self):
        self.assertEqual(git.get_repo_owner(), 'smaant')

    def test_get_repo_name(self):
        self.assertEqual(git.get_repo_name(), 'cmdpr')
