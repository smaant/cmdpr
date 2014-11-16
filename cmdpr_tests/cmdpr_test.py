# coding: utf-8
from unittest import TestCase

import yaml
from cmdpr_tests import get_resource_path
from cmdpr import pullrequest


class CmdprTestCase(TestCase):

    def test_extract_title_and_body(self):
        data = yaml.load(open(get_resource_path('commits.yaml')).read())
        for case in data:
            self.assertEqual(
                pullrequest.extract_title_and_body(case['text']),
                (case['title'], case['body']))