from general import *
import requests
import json
from datetime import datetime, timedelta
from model import *
def get_commit_from_remote(url):
    """
    从远端查询仓库的提交信息
    :param url: 仓库地址
    :return:
    """

    api = getApiUrl(url, 'commits')
    api_request = requests.get(url=api)
    owner_name, repo_name = getRepoInfo(url)
    if api_request.ok:
        contents = json.loads(api_request.content)
        if contents:
            owner = contents['owner']['login']  # owner's id
            avatar_url = contents['owner']['avatar_url']  # 头像地址
            html_url = contents['owner']['html_url']  # github用户地址
            description = contents['description']
            topics = contents['topics']
            stargazers_count = contents['stargazers_count']  # number of star
            created_at = contents['created_at']
            content_id = contents['id']
            forks_count = contents['forks_count']
            watchers_count = contents['watchers_count']
            committers = {}
            date_list = []
            for committer in contents:
                committer_id = committer["sha"]
                date_it = committer['commit']['author']['date']
                date = list(date_it)
                date.pop(10)  # pop 'T'
                date.pop(18)  # pop 'Z'
                date_list.append(datetime.strptime("".join(date), "%Y-%m-%d%H:%M:%S"))
                db.session.merge(
                    Commits(id=committer_id, owner_name=owner_name,
                            repo_name=repo_name,
                            con_name=committer['commit']['author']['name']
                            )
                )

                # 获取并插入时间，对字符串处理一下存进数据库
                date1 = datetime.strptime(committer['commit']['author']['date'][0:10]
                                          + ""
                                          + committer['commit']['author']['date'][11:19],
                                          "%Y-%m-%d%H:%M:%S")
                # db.session.add(
                db.session.merge(
                    date01(id=committer_id,
                           repo_name=owner_name,
                           date_newest=date1,
                           date_local=datetime.now(),
                           date_lasttime=date1
                           )
                )

