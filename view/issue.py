import requests
import json
from general import *

def get_issues(url):
    """
    获取某个仓库的所有issue
    :return: issue list
    """
    param = {
        "per_page": 100,  # get 100 issues per page
        "page": 1,  # get from the first page
        "state": "all"  # get both open&closed issues
    }
    issues = []
    issue_url = getApiUrl(url, 'issues')
    issue_request = requests.get(url=issue_url, params=param)
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

def textForCloud(url):
    res = ''
    issues = get_issues(url)
    for issue in issues:
        res += issue["title"]
    return res
