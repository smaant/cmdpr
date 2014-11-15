# coding: utf-8
import os
import logging


handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logging.disable(logging.CRITICAL)


def get_root_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))