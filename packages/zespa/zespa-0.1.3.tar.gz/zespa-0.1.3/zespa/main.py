import csv

import fire
from beautifultable import BeautifulTable
from tqdm import tqdm

from configuration import ZespaConfiguration
from github_requester import GitHubRequester
from issue import Issue
from zenhub_requester import ZenHubRequester


class Zespa():
    def __init__(self):
        self._config = ZespaConfiguration()

    def configure(self):
        self._config.create()
        return 'OK'

    def aggregate(self, start_date, end_date, *labels):
        self._config.check()
        github_token = self._config.get_github_token()
        zenhub_token = self._config.get_zenhub_token()
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        labels = self._parse_label_args(labels)

        issue_list = []
        repo_names = self._config.get_repo_names()
        for repo_name in repo_names:
            github_requester = GitHubRequester(repo_name, github_token)
            repo_id = github_requester.get_repo_id()
            zenhub_requester = ZenHubRequester(repo_id, zenhub_token)
            github_issues = github_requester.get_issues(start_date, end_date)

            for g_issue in tqdm(github_issues):
                if g_issue['milestone'] is None:
                    continue
                issue = Issue(id=g_issue['number'],
                              labels=[label_info['name'] for label_info in g_issue['labels']])
                issue.title = g_issue['title']
                issue.estimate = zenhub_requester.get_estimate(issue.id)
                issue_list.append(issue)

        filtered, omitted = self._filter(labels, issue_list)

        self._print_table(' or '.join(labels), filtered)
        self._print_table('Not ' + ' or '.join(labels), omitted)
        label_str = '_'.join(labels)
        self._export_csv(f'{start_date}-{end_date}-{label_str}', filtered)
        self._export_csv(f'{start_date}-{end_date}-Not_{label_str}', omitted)

    def _parse_label_args(self, labels):
        aggregation_groups = []
        index = -1
        for label in labels:
            if label == '--labels':
                aggregation_groups.append([])
                index += 1
            else:
                aggregation_groups[index].append(label)
        assert len(aggregation_groups) == 1
        return aggregation_groups[0]

    def _filter(self, labels, issue_list):
        """
        issue_list の中で
        labels のラベルを持つものを第一返り値
        labels のラベルを持たないものを第二返り値として返す
        """
        filtered = []
        omitted = []
        for issue in issue_list:
            is_filtered = False
            for label in issue.labels:
                if label in labels:
                    is_filtered = True
                    filtered.append(issue)
                    break
                elif labels[0].lower() == 'all':
                    is_filtered = True
                    filtered.append(issue)
                    break
            if not is_filtered:
                omitted.append(issue)

        return filtered, omitted

    def _print_table(self, title, issue_list):
        table = BeautifulTable()
        table.column_headers = [title]
        sum_estimate = sum([issue.estimate for issue in issue_list])
        table.append_row([sum_estimate])
        print(table)
        return True

    def _export_csv(self, title, issue_list):
        f = open(f'{title}.csv', 'w', encoding='shift_jis')
        writer = csv.writer(f)
        writer.writerow(['タスクのタイトル', 'タスクの複雑さ'])
        for issue in issue_list:
            try:
                writer.writerow([issue.title, issue.estimate])
            except Exception as e:
                print(e)
                print("Can not Encode: " + issue.title)
        f.close()
        return True


def main():
    fire.Fire(Zespa(), name='zespa')


if __name__ == '__main__':
    main()
