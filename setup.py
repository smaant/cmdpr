#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

import cmdpr


setup(
    name='cmdpr',
    version=cmdpr.version,
    description='Creates GitHub pull request for current branch in current git repository',

    packages=find_packages(),
    entry_points={
        'console_scripts': ['cmdpr = cmdpr.pullrequest:pull_request']
    },

    install_requires=['requests'],
    tests_require=['PyYAML'],
    zip_safe=False,

    author='Anton Panferov',
    author_email='smaant@gmail.com',
    url=cmdpr.repo_url
)