from general import *
import requests
import json
from datetime import datetime
from flask import Blueprint, request
from model import *

blueprint = Blueprint("commits", __name__)

headers = {}
try:
    with open('token', 'r') as token_file:  # 本地有token文件，就用token，没有token就直接查询
        token = token_file.readline()
        headers = {
            "Authorization": token
        }
except FileNotFoundError:
    pass


@blueprint.route('/commits', methods=['GET', 'POST'])
def updateCommit():
    data = eval(request.get_data())  # dangerous!!!!!
    url = data.get('url')
    return getRemoteCommit(url)


def getRemoteCommit(url):
    """
    从远端查询仓库的提交信息
    :param url: 仓库地址
    :return:
    """
    u_list = url.split('/')
    api = getApiUrl(url, '')[:-1]
    api_request = requests.get(url=api,headers=headers)
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
            api = getApiUrl(url, 'commits')
            api_request = requests.get(url=api,headers=headers)
            contents = json.loads(api_request.content)
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

                date1 = datetime.strptime(committer['commit']['author']['date'][0:10] + ""
                                          + committer['commit']['author']['date'][11:19],
                                          "%Y-%m-%d%H:%M:%S")
                # db.session.add(
                db.session.merge(
                    date01(id=id, repo_name=u_list[-1], date_newest=date1, date_local=datetime.now(),
                           date_lasttime=date1)
                )

            sorted_date = sorted(date_list, reverse=True)
            date_newest = sorted_date[0]
            for committer in contents:
                if committer.get('author') is None or committer.get('author').get('login') is None:
                    #  bug-fixed: 删除文件的记录也会在api_ret中，且其author为null，应该舍去
                    continue
                key = committer.get('author').get('login')
                if committers.get(key) is None:
                    committers[key] = 1
                else:
                    committers[key] += 1

            sorted_dict = sorted(committers.items(), key=lambda kv: (kv[1], kv[0]),
                                 reverse=True)  # 按(kv[1], kv[0])降序排序
            target = u_list[3] + '/' + u_list[4]

            commit_users = []
            for i in range(0, len(sorted_dict)):
                if sorted_dict[i]:
                    commit_url = 'https://github.com/' + sorted_dict[i][0]
                    api_request = requests.get('https://api.github.com/users/' + sorted_dict[i][0],headers=headers)
                    user_info = json.loads(api_request.content)
                    avatar_url_1 = user_info['avatar_url']
                    commit_users.append({"user": sorted_dict[i][0], "url": commit_url, "a_url": avatar_url_1})
            # db.session.flush()
            try:
                db.session.commit()
            except:
                db.session.rollback()
            # db.session.flush()
            return {"success": True,
                    "message": "success!",
                    "target": target,
                    "id": content_id,
                    "url": url,
                    "owner": owner,
                    "avatar_url": avatar_url,
                    "html_url": html_url,
                    "description": description,
                    "topics": topics,
                    "stargazers_count": stargazers_count,
                    "created_at": created_at,
                    "commit_users": commit_users,
                    "date_newest": date_newest,
                    "forks_count": forks_count,
                    "watchers_count": watchers_count
                    }, 200

    else:
        return {
                   "success": False,
                   "message": "Fail"
               }, 404


def getLocalCommit(url):
    owner_name, repo_name = getRepoInfo(url)
    return None  # to be added
