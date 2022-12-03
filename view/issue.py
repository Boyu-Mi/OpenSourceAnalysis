import requests
import json
from flask import Blueprint, request
from general import getApiUrl

blueprint = Blueprint("issues", __name__)


@blueprint.route('/issues/', methods=['GET', 'POST'])
def issues():
    data = eval(request.get_data())  # dangerous!!!!!
    url = data.get('url')
    return get_issues(url)


def get_issues(url):
    """
    获取某个仓库的所有issue
    :return: [{
        "body": "### 🐛 Describe the bug\n\nTo be filled out, realized this as I was falling asleep. \n\n### Versions\n\nNo",
        "title": "AOTAutograd input dedup needs a strategy for fake tensor args"
        }]
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
    return issues, 200


def textForCloud(url):
    res = ''
    issues_ = get_issues(url)
    for issue in issues_:
        res += issue["title"]
    return res
