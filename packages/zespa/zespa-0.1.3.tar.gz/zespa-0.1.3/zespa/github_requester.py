import json

import requests

GITHUB_SEARCH_API = 'https://api.github.com/search/issues'
GITHUB_REPO_API = 'https://api.github.com/repos'
PER_PAGE = 100


class GitHubRequester():
    def __init__(self, repo_name, token):
        self.repo_name = repo_name
        self.token = token

    def get_issues(self, start_date, end_date):
        """
        start_date から end_date までのIssueをすべて取得する
        """
        page = 1
        issues = []
        while True:
            issues += self._fetch_issues(start_date, end_date, page)
            if issues == [] or len(issues) % PER_PAGE != 0:
                break
            page += 1
        return issues

    def _fetch_issues(self, start_date, end_date, page=1):
        headers = { 'Authorization': f'token {self.token}' }
        url = f'{GITHUB_SEARCH_API}?per_page={PER_PAGE}&page={page}' \
              f'&q=is:issue+is:closed+closed:{start_date}..{end_date}+repo:{self.repo_name}'
        resp = requests.get(url=url, headers=headers)
        issues = json.loads(resp.content.decode('utf-8'))
        try:
            return issues['items'] or []
        except KeyError:
            if 'errors' in issues:
                for error in issues['errors']:
                    print(error['message'])
            return []

    def get_repo_id(self):
        resp = requests.get(f'{GITHUB_REPO_API}/{self.repo_name}?access_token={self.token}')
        repo = json.loads(resp.content.decode('utf-8'))
        try:
            return repo['id']
        except KeyError:
            if 'errors' in repo:
                for error in repo['errors']:
                    print(error['message'])
