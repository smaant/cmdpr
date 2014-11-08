# coding: utf-8
import requests

from cmdpr import git

GITHUB_API_HOST = 'https://api.github.com'
USER_AGENT = 'cmdpr 0.1'


class GitHub:

    def __init__(self, token):
        self.repo_owner = git.get_repo_owner()
        self.repo_name = git.get_repo_name()

        self.session = requests.Session()
        self.session.auth = (token, '')
        self.session.headers = {'User-Agent': USER_AGENT}

    def _do_get(self, url):
        """
        :rtype: requests.Response
        """
        return self.session.get(GITHUB_API_HOST + url)

    def is_token_valid(self):
        return self._do_get('/user').status_code == 200

    def create_pull_request(self, base, head, title, body=None):
        pass


