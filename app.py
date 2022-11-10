from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin  # 处理跨域
import requests
import json
import config
from datetime import datetime, timedelta
import calendar
import os
from model import db
from model import *
import re

app = Flask(__name__)

basedir = os.path.abspath(app.root_path)
# config databases
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True  # 显示原始SQL语句
app.config.from_object(config)  # 读取配置
db.init_app(app)
cors = CORS(app, supports_credentials=True)  #支持跨域

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
    url = url.strip('/')
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
    url = url.strip('/')
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
    db.create_all()  # 新建数据库
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
    ret["created_at"] = user_info["created_at"][0:10]+' '+user_info["created_at"][11:19]
    ret["updated_at"] = user_info["updated_at"][0:10]+' '+user_info["updated_at"][11:19]
    time = datetime.now()
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")
    ret["time"] = timestr

    date_c = datetime.strptime(ret["created_at"],
                               "%Y-%m-%d %H:%M:%S")
    date_u = datetime.strptime(ret["updated_at"],
                               "%Y-%m-%d %H:%M:%S")
    # 存储信息到数据库
    db.session.merge(
        User(id=ret["id"], user_type=ret["user_type"],
             name=user_name, company=ret["company"],
             avatar_url=ret["avatar_url"], created_at=date_c, updated_at=date_u,
             follower_number=ret["follower_number"], public_repo_number=ret["public_repo_number"], time=time)
    )
    db.session.commit()

    return ret, 200


''' 
    r = requests.get(github_url)
    print(r.links)
有>1页, 在第一页:
{
    'next': {'url': 'https://api.github.com/repositories/65600975/commits?per_page=100&page=2', 'rel': 'next'},
    'last': {'url': 'https://api.github.com/repositories/65600975/commits?per_page=100&page=536', 'rel': 'last'}
}
有>1页, 在最后一页(无last):
{
    'first': {'url': 'https://api.github.com/repositories/65600975/commits?page=1&per_page=100', 'rel': 'first'},
    'prev': {'url': 'https://api.github.com/repositories/65600975/commits?page=535&per_page=100', 'rel': 'prev'}}
}
有>2页, 在中间页:
{
    'next': {'url': 'https://api.github.com/repositories/65600975/commits?page=536&per_page=100', 'rel': 'next'},
    'last': {'url': 'https://api.github.com/repositories/65600975/commits?page=536&per_page=100', 'rel': 'last'},
    'first': {'url': 'https://api.github.com/repositories/65600975/commits?page=1&per_page=100', 'rel': 'first'},
    'prev': {'url': 'https://api.github.com/repositories/65600975/commits?page=534&per_page=100', 'rel': 'prev'}
}
总共就1页, 在那一页:(无last)
{}
'''
@app.route('/commit_by_time/', methods=['GET', 'POST'])
def commit_by_time():
    # 返回: total_commit 按时间的commit数, 默认起止年月日，输入允许为空（不传对应参数即可。）
    # db.create_all()  # 新建数据库
    data = request.json
    year_from = data.get("year_from") # 都是整数
    year_to = data.get("year_to")
    month_from = data.get("month_from")
    month_to = data.get("month_to")
    day_from = data.get("day_from")
    day_to = data.get("day_to")
    time_unit = data.get("time_unit")  # 最小统计单位，year,month,day
    url = data.get('url')
    url = url.strip('/')
    if url is None:
        return {
                   "success": False,
                   "message": "No url!"
               }, 404
    # process the url
    u_list = url.split('/')
    commit_url = 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/commits'  # the url to get commit info
    
    # handle exceptions while getting commit info
    if 'github.com' not in u_list:
        return {
                   "success": False,
                   "message": "Invalid github repo ink!"
               }, 404
    try:
        api_request = requests.get(url=commit_url, headers=headers, timeout=5)
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
    try:
        date_from, date_to = get_complete_date(time_unit,year_from,year_to,month_from,month_to,day_from,day_to)
    except ValueError:
        return {
                    "success": False,
                    "message": "Date out of range!"
                }, 404
    except TypeError:
        return {
                    "success": False,
                    "message": "Time unit invalid!"
                }, 404
    try:
        commit_count_by_time = get_commit_by_time(date_from,date_to,u_list)
    except requests.exceptions.ReadTimeout:
        return {
                   "success": False,
                   "message": "Timeout!"
               }, 404
    except requests.exceptions.HTTPError:
        return {
                   "success": False,
                   "message": "Fail to get info! The repo may not exist."
               }, 404
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = u_list[-1]
    ret["owner_name"] = u_list[-2]
    ret["commit_count_by_time"] = commit_count_by_time
    
    date_all_from, date_all_to = get_complete_date("year",None,None,None,None,None,None)
    try:
        commit_count_total = get_commit_by_time(date_all_from,date_all_to,u_list)
    except requests.exceptions.ReadTimeout:
        return {
                   "success": False,
                   "message": "Timeout!"
               }, 404
    except requests.exceptions.HTTPError:
        return {
                   "success": False,
                   "message": "Fail to get info! The repo may not exist."
               }, 404
    ret["commit_count_total"] = commit_count_total
    time = datetime.now()
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")
    ret["time"] = timestr
    
    # 存储到数据库
    db.session.merge(
        Commit_count(repo_name=u_list[-1],owner_name=u_list[-2],
        commit_total=commit_count_total,commit_by_time=commit_count_by_time,
        date_from=datetime.strptime(date_from,"%Y-%m-%dT%H:%M:%SZ"),
        date_to=datetime.strptime(date_to,"%Y-%m-%dT%H:%M:%SZ"),
        time=time)
    )
    db.session.commit()
    
    return ret, 200

def get_complete_date(time_unit,year_from,year_to,month_from,month_to,day_from,day_to):
    try: #判断日期合法性
        # 处理空值
        if year_from is None:
                year_from = 2000 # github创建时间2008
        if year_to is None:
            year_to = datetime.today().year
        if month_from is None:
            month_from = 1
        if month_to is None:
            month_to = 12
        if day_from is None:
            day_from = 1
        if day_to is None:
            weekday,day_to = calendar.monthrange(year_to,month_to)
        if time_unit == "year":
            date_from = datetime(year_from,1,1,0,0,0)
            date_to = datetime(year_to+1,1,1,0,0,0)
        elif time_unit == "month":
            date_from = datetime(year_from,month_from,1,0,0,0)
            
            if month_to == 12:
                year_to += 1
                month_to = 1
            date_to = datetime(year_to,month_to,1,0,0,0)
        elif time_unit == "day":
            date_from = datetime(year_from,month_from,day_from,0,0,0)
            date_to = datetime(year_to,month_to,day_to,0,0,0)+timedelta(days=1)
        else:
            raise TypeError
    except ValueError:
        raise
    date_from =date_from.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_to = date_to.strftime("%Y-%m-%dT%H:%M:%SZ")
    return (date_from,date_to)

def get_commit_by_time(date_from,date_to,u_list):
    param = {"per_page":100, "since":date_from, "until":date_to} # 按时间获取请求的参数
    #获取commit数据
    commit_url = 'https://api.github.com/repos/' + u_list[-2]+'/'+u_list[-1] + '/commits'
    try:
        commit_request = requests.get(url=commit_url, headers=headers, timeout=5, params=param)
    except requests.exceptions.ReadTimeout:
        raise
    if not commit_request.ok:
        raise requests.exceptions.HTTPError
    commit_info = json.loads(commit_request.content)
    if len(commit_request.links) == 0: # 字典为空，返回值为{}，只有一页
        commit_count = len(commit_info)
    else: # 大于一页，获取页数
        last_str = commit_request.links['last']['url']
        per_page = int(re.search('per_page=[0-9]+',last_str).group()[9:])
        last_page = int(re.search('[^a-z_]page=[0-9]+',last_str).group()[6:])
        # 请求最后一个page
        try:
            last_request = requests.get(url=commit_url+"?page="+str(last_page), headers=headers, timeout=5, params=param)
        except requests.exceptions.ReadTimeout:
            raise
        if not last_request.ok:
            raise requests.exceptions.HTTPError
        last_info = json.loads(last_request.content)
        commit_count = len(last_info)
        commit_count += per_page * (last_page-1)
    return commit_count

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
