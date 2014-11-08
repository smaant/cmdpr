# coding: utf-8
import os


def get_resources_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')