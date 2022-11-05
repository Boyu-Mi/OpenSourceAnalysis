from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin  # 处理跨域
import requests
import json
import config
from datetime import datetime
import os
from model import db
from model import *

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)  #支持跨域
basedir = os.path.abspath(app.root_path)
# config databases
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True  # 显示原始SQL语句
app.config.from_object(config)  # 读取配置
db.init_app(app)


@app.route('/commit', methods=['POST'])
def commit():
    """

    :return:
    """
    # db.create_all()  # 新建数据库
    # get prams from request
    data = request.json
    url = data.get('url')  #输入的仓库地址
    if url is None:
        return {
            "success": False,
            "message": "No url!"
        }
    num_layout = data.get('num_layout')  #显示的数量？
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
        api_request = requests.get(url=content_url, timeout=5)
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
        avatar_url = contents['owner']['avatar_url']
        html_url = contents['owner']['html_url']
        description = contents['description']
        topics = contents['topics']
        stargazers_count = contents['stargazers_count']  # number of star
        created_at = contents['created_at']
        content_id = contents['id']
        # noinspection DuplicatedCode
        try:
            api_request = requests.get(url=api_url, timeout=5, params={"per_page": 100})
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
        committer_dict = {}
        date_list = []
        for committer in api_ret:
            date_it = committer['commit']['author']['date']
            date = list(date_it)
            date.pop(10)  # pop 'T'
            date.pop(18)  # pop 'Z'
            date_list.append(datetime.strptime("".join(date), "%Y-%m-%d%H:%M:%S"))

            # 数据插入数据库,commits的数据
            db.session.add(
                Commits(owner_name=u_list[-2], repo_name=u_list[-1], con_name=committer['commit']['author']['name'])
            )

            # 获取并插入时间，对字符串处理一下存进数据库
            date1 = datetime.strptime(committer['commit']['author']['date'][0:10] + ""
                                      + committer['commit']['author']['date'][11:19],
                                      "%Y-%m-%d%H:%M:%S")
            db.session.add(
                date01(repo_name=u_list[-1], date_newest=date1, date_local=datetime.now(), date_lasttime=date1)
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

        sorted_dict = sorted(committer_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
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
                "date_newest": date_newest
                }, 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
