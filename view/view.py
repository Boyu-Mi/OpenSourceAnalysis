import requests
import json


def get_issues():
    """
    获取某个仓库的所有issue
    :return: issue list
    """
    # for test
    url = 'https://github.com/tianzhi0549/FCOS'
    header = {
        "Authorization":
            'bearer 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'
    }
    param = {
        "per_page": 100,  # get 100 issues per page
        "page": 1,  # get from the first page
        "state": "all"  # get both open&closed issues "all" or "open" or "closed"
    }
    issues = []
    u_list = url.strip('/').split('/')
    issues_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/issues'
    try:
        issue_request = requests.get(url=issues_url, headers=header, timeout=5, params=param)
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


def get_pulls():
    url = 'https://github.com/pytorch/pytorch'
    header = {
        "Authorization":
            'bearer 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'
    }
    pull_requests = []
    u_list = url.strip('/').split('/')
    pr_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/pulls'
    param = {
        "per_page": 100,  # get 100 issues per page
        "page": 1,  # get from the first page
        "state": "all"  # get both open&closed prs "all" or "open" or "closed"
    }
    try:
        pr_request = requests.get(url=pr_url, headers=header, timeout=5, params=param)
    except requests.exceptions.ReadTimeout:
        raise
    if not pr_request.ok:
        raise requests.exceptions.HTTPError
    issues_of_this_page = json.loads(pr_request.content)
    for issue in issues_of_this_page:
        if issue['body'] is not None:
            pull_requests.append(
                {
                    "title": issue['title'],  # title of the issue
                    "body": issue['body']  # body of the issue
                }
            )
    return pull_requests





