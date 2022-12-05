import requests
import json
from general import *
from model import *
def getRemoteIssues(url):
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
    owner_name, repo_name = getRepoInfo(url)
    for issue in issues_of_this_page:
        if issue['body'] is not None:
            issues.append(
                {
                    "title": issue['title'],  # title of the issue
                    "body": issue['body']  # body of the issue
                }
            )
        issue_id = issue['number']
        db.session.merge(
            Issue(owner_name=owner_name, repo_name=repo_name, id=issue_id, title=issue['title'], body=issue['body'])
        )
    db.session.commit()
    return issues


def getLocalIssue(url):
    owner_name, repo_name = getRepoInfo(url)
    issue_list = db.session.query(Contributors).filter_by(owner_name=owner_name,
                                                          repo_name=repo_name).all()
    res = ""
    for issue in issue_list:
        res += issue.title
    return res


def textForCloud(url):
    return getLocalIssue(url)
