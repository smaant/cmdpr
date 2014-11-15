# coding: utf-8
import os
import json
import logging

logger = logging.getLogger(__name__)


class CmdprConfig:

    def __init__(self, path):
        self.config_path = path
        self.data = {}
        if os.path.exists(self.config_path):
            logger.debug('Loading config')
            with open(self.config_path) as f:
                self.data = json.loads(f.read())
                logger.debug('Config: {}'.format(self.data))

    def get(self, key, fallback=None):
        return self.data.get(key, fallback)

    def put(self, key, value):
        self.data[key] = value

    def save(self):
        logger.debug('Save config file')
        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        with open(self.config_path, mode='wt') as f:
            f.write(json.dumps(self.data, indent=4))