from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
import os

from flask_cors import CORS

from model import db
from model import *

app = Flask(__name__)
basedir = os.path.abspath(app.root_path)
# config databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors = CORS(app, supports_credentials=True)  # 支持跨域

headers = {}
try:
    with open('token', 'r') as token_file:  # 本地有token文件，就用token，没有token就直接查询
        token = token_file.readline()
        headers = {
            "Authorization": token
        }
except FileNotFoundError:
    pass


@app.route('/commit/', methods=['GET', 'POST'])
def commit():
    """

    :return:
    """
    # get prams from request
    data = request.json
    url = data.get('url')
    if url is None:
        return {
                   "success": False,
                   "message": "No url!"
               }, 404  # 这里之前没加404，是有什么原因吗？先补上
    num_layout = data.get('num_layout')  # 展示的突出贡献者的数量
    if num_layout is None:
        num_layout = 3

    # process the url
    u_list = url.split('/')
    api_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/commits'  # the url to get commit info
    content_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1]  # the url to get content info

    # handle exceptions while getting commit info
    if 'github.com' not in u_list:
        return {
                   "success": False,
                   "message": "Invalid github repo ink!"
               }, 404
    try:
        api_request = requests.get(url=content_url, headers=headers, timeout=5)
    except requests.exceptions.ReadTimeout:
        # timeout exception(max time is 5s)
        return {
                   "success": False,
                   "message": "Timeout!"
               }, 404
    if not api_request.ok:
        # invalid result
        return {
                   "success": False,
                   "message": "Fail to get info!"
               }, 404

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
        # noinspection DuplicatedCode
        try:
            api_request = requests.get(url=api_url, headers=headers, timeout=5, params={"per_page": 100})
        except requests.exceptions.ReadTimeout:
            # timeout exception(max time is 5s)
            return {
                       "success": False,
                       "message": "Timeout!"
                   }, 404
        if not api_request.ok:
            # invalid result
            return {
                       "success": False,
                       "message": "Fail to get info!"
                   }, 404
        api_ret = json.loads(api_request.content)
        committer_dict = {}  # 字典{提交者 : 提交数量}
        date_list = []
        for committer in api_ret:
            id = committer["sha"]
            date_it = committer['commit']['author']['date']
            date = list(date_it)
            date.pop(10)  # pop 'T'
            date.pop(18)  # pop 'Z'
            date_list.append(datetime.strptime("".join(date), "%Y-%m-%d%H:%M:%S"))

            # 数据插入数据库,commits的数据
            # db.session.add(
            # 改add为merge，若无则add,若有则update，这样避免数据库太大
            db.session.merge(
                Commits(id=id, owner_name=u_list[-2], repo_name=u_list[-1],
                        con_name=committer['commit']['author']['name'])
            )

            # 获取并插入时间，对字符串处理一下存进数据库
            date1 = datetime.strptime(committer['commit']['author']['date'][0:10] + ""
                                      + committer['commit']['author']['date'][11:19],
                                      "%Y-%m-%d%H:%M:%S")
            # db.session.add(
            db.session.merge(
                date01(id=id, repo_name=u_list[-1], date_newest=date1, date_local=datetime.now(), date_lasttime=date1)
            )

        sorted_date = sorted(date_list, reverse=True)
        date_newest = sorted_date[0]
        # 插入数据库date_newest与u_list[3],u_list[4]
        for committer in api_ret:
            if committer.get('author') is None or committer.get('author').get('login') is None:
                #  bug-fixed: 删除文件的记录也会在api_ret中，且其author为null，应该舍去
                continue
            key = committer.get('author').get('login')
            if committer_dict.get(key) is None:
                committer_dict[key] = 1
            else:
                committer_dict[key] += 1

        sorted_dict = sorted(committer_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)  # 按(kv[1], kv[0])降序排序
        target = u_list[3] + '/' + u_list[4]

        commit_users = []
        for i in range(0, min(num_layout, len(sorted_dict))):
            if sorted_dict[i]:
                commit_url = 'https://github.com/' + sorted_dict[i][0]
                api_request = requests.get('https://api.github.com/users/' + sorted_dict[i][0])
                user_info = json.loads(api_request.content)
                avatar_url_1 = user_info['avatar_url']
                commit_users.append({"user": sorted_dict[i][0], "url": commit_url, "a_url": avatar_url_1})
        db.session.commit()
        return {"success": True, "message": "success!",
                "target": target, "id": content_id, "url": url, "owner": owner, "avatar_url": avatar_url,
                "html_url": html_url, "description": description, "topics": topics,
                "stargazers_count": stargazers_count, "created_at": created_at, "commit_users": commit_users,
                "date_newest": date_newest, "forks_count": forks_count,
                "watchers_count": watchers_count
                }, 200


@app.route('/contributors/', methods=['GET', 'POST'])
def contributors():
    """
    返回仓库的贡献者
    :return:
    [
    (contributor1.id, contributor1.number_of_contributions),
    (contributor2.id, contributor2.number_of_contributions),
    ...
    ]
    """
    data = request.json
    url = data.get('url')
    if url is None:
        return {
                   "success": False,
                   "message": "No url!"
               }, 404
    threshold = 0.2
    u_list = url.split('/')
    contributor_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/contributors'
    repo_info_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1]
    # handle exceptions while getting commit info
    if 'github.com' not in u_list:
        return {
                   "success": False,
                   "message": "Invalid github repo ink!"
               }, 404
    try:
        contributor_info_request = requests.get(url=contributor_url, headers=headers, timeout=5)
        repo_info_request = requests.get(url=repo_info_url, headers=headers, timeout=5)
    except requests.exceptions.ReadTimeout:
        # timeout exception(max time is 5s)
        return {
                   "success": False,
                   "message": "Timeout!"
               }, 404
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
                (item['login'], item['contributions'])
            )
            db.session.merge(
                Contributors(
                    owner_name=repo_info['owner']['login'],
                    repo_name=repo_info['name'],
                    con_name=item['login'],
                    con_num=item['contributions']
                )
            )
        db.session.commit()
        return {"success": True,
                "message": "success!"
                }, 200


@app.route('/user/', methods=['GET', 'POST'])
def user():
    # 获取某个用户的信息，包括organization，company
    # db.create_all()  # 新建数据库
    data = request.json
    user_name = data.get("user_name")
    if user_name is None:  # 没输入用户名
        return {
                   "success": False,
                   "message": "No user name!"
               }, 404
    # 用户名存在
    user_url = "https://api.github.com/users/" + user_name
    try:
        user_request = requests.get(url=user_url, headers=headers, timeout=5)
        # print(headers) # debug
    except requests.exceptions.ReadTimeout:
        # timeout exception(max time is 5s)
        return {
                   "success": False,
                   "message": "Timeout!"
               }, 404
    if not user_request.ok:
        # invalid result，可能的原因是该用户名不存在
        return {
                   "success": False,
                   "message": "Fail to get info! The user may not exist."
               }, 404
    user_info = json.loads(user_request.content)
    ret = {"success": True, "message": "success!", "user_name": user_name}
    ret["id"] = user_info["id"]
    ret["avatar_url"] = user_info["avatar_url"]
    ret["user_url"] = user_info["html_url"]
    ret["user_type"] = user_info["type"]  # Organization,User等
    ret["company"] = user_info["company"]
    ret["public_repo_number"] = user_info["public_repos"]
    ret["follower_number"] = user_info["followers"]
    ret["created_at"] = user_info["created_at"]
    ret["updated_at"] = user_info["updated_at"]
    date_c = datetime.strptime(ret["created_at"][0:10]
                               + ret["created_at"][11:19],
                               "%Y-%m-%d%H:%M:%S")
    date_u = datetime.strptime(ret["updated_at"][0:10]
                               + ret["updated_at"][11:19],
                               "%Y-%m-%d%H:%M:%S")
    # 存储信息到数据库
    db.session.merge(
        User(id=ret["id"], user_type=ret["user_type"],
             name=user_name, company=ret["company"],
             avatar_url=ret["avatar_url"], created_at=date_c, updated_at=date_u,
             follower_number=ret["follower_number"], public_repo_number=ret["public_repo_number"])
    )
    db.session.commit()

    return ret, 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
