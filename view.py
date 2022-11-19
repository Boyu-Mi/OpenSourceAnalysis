import requests
import json


def get_issues():
    """
    获取某个仓库的所有issue
    :return: issue list
    """
    url = 'https://github.com/tianzhi0549/FCOS'
    header = {
        "Authorization":
            'bearer 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'
    }
    param = {
        "per_page": 100,  # get 100 issues per page
        "page": 1,  # get from the first page
        "state": "all"  # get both open&closed issues
    }
    issues = []
    u_list = url.strip('/').split('/')
    commit_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/issues'
    try:
        issue_request = requests.get(url=commit_url, headers=header, timeout=5, params=param)
    except requests.exceptions.ReadTimeout:
        raise
    if not issue_request.ok:
        raise requests.exceptions.HTTPError
    issues_of_this_page = json.loads(issue_request.content)
    for issue in issues_of_this_page:
        if issue['body'] is not None:
            issues.append(
                {
                    "title": issue['title'],  # title of the issue
                    "body": issue['body']  # body of the issue
                }
            )
    return issues
