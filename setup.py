#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages


setup(
    name="cmdpr",
    version="0.1",
    description='Creates GitHub pull request for current branch in current git repository',

    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['cmdpr = cmdpr.cmdpr:pull_request']
    },

    install_requires=['requests'],
    zip_safe=False,

    author='Anton Panferov',
    author_email='smaant@gmail.com',
    url='https://github.com/smaant/cmdpr'
)