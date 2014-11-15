# coding: utf-8
import json
import logging

import requests


GITHUB_API_HOST = 'https://api.github.com'
USER_AGENT = 'cmdpr 0.3'

logger = logging.getLogger(__name__)


class GitHub:

    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': USER_AGENT}

        if token is not None:
            self.session.auth = (token, '')

    def _do_get(self, url):
        """
        :rtype: requests.Response
        """
        return self.session.get(GITHUB_API_HOST + url)

    def _do_post(self, url, data=None):
        """
        :rtype: requests.Response
        """
        return self.session.post(GITHUB_API_HOST + url, data=json.dumps(data))

    def _do_post_with_auth(self, url, auth, headers, data):
        """
        :rtype: requests.Response
        """
        all_headers = dict(headers.items() + self.session.headers.items())
        authorization_url = GITHUB_API_HOST + url

        logger.debug('POST {} (headers={}, data={})'.format(authorization_url, all_headers, data))
        response = requests.post(authorization_url, data=json.dumps(data), auth=auth, headers=all_headers)
        logger.debug('got {}: {} ({})'.format(response.status_code, response.reason, response.text))
        return response

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
        response = self._do_post(url, data)
        if response.status_code != 201:
            raise GitHubException(self._extract_error_message(response))
        else:
            data = response.json()
            return data['html_url']

    def create_token(self, login, password, one_time_password=''):
        data = {
            'scopes': ['repo'], 'note': 'cmdpr', 'note_url': 'https://github.com/smaant/cmdpr'
        }
        response = self._do_post_with_auth('/authorizations', (login, password),
                                           {'X-GitHub-OTP': one_time_password}, data)
        response_data = response.json()
        if response.status_code == 401 and 'X-GitHub-OTP' in response.headers:
            return None
        elif 'token' in response_data:
            return response_data['token']
        else:
            raise GitHubException(self._extract_error_message(response))


class GitHubException(Exception):
    def __init__(self, message):
        super(GitHubException, self).__init__(message)