# coding: utf-8
import json

import requests


GITHUB_API_HOST = 'https://api.github.com'
USER_AGENT = 'cmdpr 0.1'


class GitHub:

    def __init__(self, token):
        self.session = requests.Session()
        self.session.auth = (token, '')
        self.session.headers = {'User-Agent': USER_AGENT}

        if not self.is_token_valid():
            raise GitHubException('GitHub token is invalid or revoked')

    def _do_get(self, url):
        """
        :rtype: requests.Response
        """
        return self.session.get(GITHUB_API_HOST + url)

    def _do_post(self, url, data=None):
        """
        :rtype: requests.Response
        """
        return self.session.post(GITHUB_API_HOST + url, data=data)

    def is_token_valid(self):
        return self._do_get('/user').status_code == 200

    def _extract_error_message(self, response):
        """
        :type response: requests.Response
        """
        data = response.json()
        for error in data.get('errors', []):
            if 'message' in error:
                return data['errors'][0]['message']

        if 'message' in data:
            return data['message']
        else:
            return 'Unknown error with code {}: {}'.format(response.status_code, response.reason)

    def create_pull_request(self, repo_info, title, base='master', body=None):
        url = '/repos/{user}/{repo}/pulls'.format(user=repo_info['owner'], repo=repo_info['name'])
        data = {
            'title': title,
            'head': repo_info['branch'],
            'base': base,
            'body': body
        }
        response = self._do_post(url, json.dumps(data))
        if response.status_code != 201:
            raise GitHubException(self._extract_error_message(response))
        else:
            data = response.json()
            return data['html_url']


class GitHubException(Exception):
    def __init__(self, message):
        super(GitHubException, self).__init__(message)