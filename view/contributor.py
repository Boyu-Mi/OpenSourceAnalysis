from general import *
import requests
import json
from model import *
from flask import Blueprint, request

blueprint = Blueprint("contributors", __name__)


@blueprint.route('/contributors/update/', methods=['GET', 'POST'])
def updateContributors():
    data = eval(request.get_data())  # dangerous!!!!!
    url = data.get('url')
    return getRemoteContributor(url)


@blueprint.route('/contributors/local/', methods=['GET', 'POST'])
def getCoreContributors():
    data = eval(request.get_data())  # dangerous!!!!!
    url = data.get('url')
    return getLocalContributor(url)


def getRemoteContributor(url):
    """
    查询贡献者
    """
    contributor_url = getApiUrl(url, 'contributors')
    repo_info_url = getApiUrl(url, '')[:-1]
    contributor_info_request = requests.get(url=contributor_url)
    repo_info_request = requests.get(url=repo_info_url)
    if not contributor_info_request.ok and not repo_info_request.ok:
        # invalid result
        return {
                   "success": False,
                   "message": "Fail to get info!"
               }, 404
    contribution_info = json.loads(contributor_info_request.content)
    repo_info = json.loads(repo_info_request.content)
    contributors_list = []
    if contribution_info:
        for item in contribution_info:
            contributors_list.append(
                {
                    "value": item['contributions'],
                    "name": item['login']
                }
            )
            if db.session.query(Contributors).filter_by(repo_name=repo_info['name'], con_name=item['login']).all():
                # 数据库中已经存在该仓库中该贡献者的信息
                db.session.query(Contributors).filter_by(repo_name=repo_info['name'], con_name=item['login']).update(
                    # 更新该仓库，该贡献者的贡献数量
                    {Contributors.con_num: item['contributions']}
                )
            else:
                # 数据库中不存在该仓库中该贡献者的信息，则添加该仓库，该贡献者的贡献数据
                db.session.add(
                    Contributors(
                        owner_name=repo_info['owner']['login'],
                        repo_name=repo_info['name'],
                        con_name=item['login'],
                        con_num=item['contributions']
                    )
                )
        db.session.commit()
        return {
                   "success": True,
                   "message": "success!",
                   "content": json.dumps(contributors_list)
               }, 200

    return {
               "success": False,
               "message": "cannot get contribution info"
           }, 404


def getLocalContributor(url):
    _, repo_name = getRepoInfo(url)
    contributors = db.session.query(Contributors).filter_by(repo_name=repo_name)
    contributors_list = []
    for contributor in contributors:
        contributors_list.append(
            {
                "value": contributor.con_num,
                "name": contributor.con_name
            }
        )

    return contributors_list, 200


@blueprint.route('/contributors/core/', methods=['GET', 'POST'])
def getCoreContributor():
    data = eval(request.get_data())  # dangerous!!!!!
    url = data.get('url')
    con_lst, _ = getLocalContributor(url)
    length = max(1, int(0.2 * len(con_lst)))
    return con_lst[:length], 200
