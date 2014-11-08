# coding: utf-8
import os


def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
