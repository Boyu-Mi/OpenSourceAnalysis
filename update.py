from flask import Blueprint,request
from datetime import datetime, timedelta
from model import *
import time
from decorators import decorator_repo,decorator_commit,decorator_stargazers,decorator_issues
import view.user
from view.contributor import updateContributors
import calendar
import requests
import json
import re

blueprint = Blueprint("update", __name__)

headers = {}
try:
    with open('token', 'r') as token_file:  # 本地有token文件，就用token，没有token就直接查询
        token = token_file.readline()
        headers = {
            "Authorization": token
        }
except FileNotFoundError:
    pass
    
@blueprint.route('/update_repo/', methods=['GET', 'POST'])
@decorator_repo
def update(u_list,data):
    # db.create_all()  # 新建数据库
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    ret = {}
    ret["success"] = True
    ret["message"] = "success"
    
    if update_commit_by_time(repo_name,owner_name) == False:
        ret["success"] = False
        ret["message"] = "Update commit_by_time failed!"
        return ret,404

    # company信息涉及的user太多了，在线获取的话要极其久（仅仅在<=1500个用户的情况下），老师只要求pytorch，不如提前update，随后的update就取消这一步
    # if update_company(repo_name,owner_name) == False:
    #     ret["success"] = False
    #     ret["message"] = "Update company failed!"
    #     return ret,404

    dic = updateContributors(u_list)[0]
    if dic["success"] == False:
        ret["success"] = False
        ret["message"] = "Update commit_by_time failed!"
        return ret,404

    # update_repo_with_url(data.get("url"))
    return ret,200

def update_repo_with_url(url):
    time.sleep(15)
    return

@decorator_commit
def get_commit_info(repo,owner,param,data = {}):
    if len(data)==0:
        return False
    for i in range(0,len(data)):
        id = data[i]["sha"]
        c_time = data[i]["commit"]["author"]["date"]
        c_time = c_time[0:10]
        result = db.session.query(Commits).filter_by(id=id).first()
        if result is not None:
            break
        db.session.merge(
            Commits(id=id,repo_name=repo,owner_name=owner,timeline=c_time)
        )
        db.session.commit()
    return True #最后一个返回值表示成功与否

def update_commit_by_time(repo_name,owner_name,data = {}):
    # date_from,date_to = get_complete_date("year", None, None, None, None, None, None)
    # total = get_commit_in_range(date_from,date_to,repo_name,owner_name)
    # page = int(total/100)+1
    page = 0
    param = {"per_page":100,"page":page}
    dict={}
    data = {}
    while(True and page <5): # 只能查看最近500条，若要更改请改page参数
        # page -= 1
        page += 1
        param = {"per_page":100,"page":page}
        data = get_commit_info(repo_name,owner_name,param)
        if data == False:
            break

    time = datetime.now()
    result = db.session.query(Commits).filter_by(repo_name=repo_name,owner_name=owner_name).all()
    for item in result:
        timelinestr = item.timeline.strftime("%Y-%m-%d")
        if timelinestr in dict.keys():
            dict[timelinestr] += 1
        else:
            dict[timelinestr] = 1
    for key,value in dict.items():
        # 存储信息到数据库
        db.session.merge(
            Commit_count(repo_name=repo_name,owner_name=owner_name,timeline=key,commit_count=value, time=time)
        )
        db.session.commit()
    return True

def update_company(repo_name,owner_name):
    
    page=0
    dict = {}
    data = {}
    while(data is not None and page <=5): # 只能查看最近500条，若要更改请改page参数
        page += 1
        param = {"per_page":100,"page":page}
        data = update_commiters(repo_name,owner_name,param,dict)
        if data[1] == False:
            return False
        dict = data[0]
    time = datetime.now()
    for key,value in dict.items():
        # 存储信息到数据库
        db.session.merge(
            Commiter_company(repo_name=repo_name,owner_name=owner_name,company=key,count=value,time=time)
        )
        db.session.commit()
    
    page=0
    dict = {}
    data = {}
    while(data is not None and page <=5): # 只能查看最近500条，若要更改请改page参数
        page += 1
        param = {"per_page":100,"page":page}
        data = update_stargazers(repo_name,owner_name,param,dict)
        if data[1] == False:
            return False
        dict = data[0]
    time = datetime.now()
    for key,value in dict.items():
        # 存储信息到数据库
        db.session.merge(
            Stargazer_company(repo_name=repo_name,owner_name=owner_name,company=key,count=value,time=time)
        )
        db.session.commit()

    page=0
    dict = {}
    data = {}
    while(data is not None and page <=5): # 只能查看最近500条，若要更改请改page参数
        page += 1
        param = {"per_page":100,"page":page}
        data = update_issues(repo_name,owner_name,param,dict)
        if data[1] == False:
            return False
        dict = data[0]
    time = datetime.now()
    for key,value in dict.items():
        # 存储信息到数据库
        db.session.merge(
            Issue_company(repo_name=repo_name,owner_name=owner_name,company=key,count=value,time=time)
        )
        db.session.commit()
    return True

@decorator_commit
def update_commiters(repo_name,owner_name,param,dict,data = {}):
    
    for i in range(0,len(data)):
        if data[i]["author"] == None:
            continue
        c_name = data[i]["author"]["login"]
        
        dic = view.user.user(c_name)[0]
        if dic["success"] == False:
            continue
        company = dic["company"] # 根据用户名获取其company名
        if(company == ""):
            continue
        if company in dict.keys():
            dict[company] += 1
        else:
            dict[company] = 1
    return dict,True

@decorator_stargazers
def update_stargazers(repo_name,owner_name,param,dict,data = {}):
    for i in range(0,len(data)):
        c_name = data[i]["login"]
        dic = view.user.user(c_name)[0]
        if dic["success"] == False:
            continue
        company = dic["company"] # 根据用户名获取其company名
        if(company == ""):
            continue
        if company in dict.keys():
            dict[company] += 1
        else:
            dict[company] = 1
    return dict,True

@decorator_issues
def update_issues(repo_name,owner_name,param,dict,data = {}):
    for i in range(0,len(data)):
        c_name = data[i]["user"]["login"]
        dic = view.user.user(c_name)[0]
        if dic["success"] == False:
            continue
        company = dic["company"] # 根据用户名获取其company名
        if(company == ""):
            continue
        if company in dict.keys():
            dict[company] += 1
        else:
            dict[company] = 1
    return dict,True

def get_complete_date(time_unit, year_from, year_to, month_from, month_to, day_from, day_to):
    try:  # 判断日期合法性
        # 处理空值
        if year_from is None:
            year_from = 2000  # github创建时间2008
        if year_to is None:
            year_to = datetime.today().year
        if month_from is None:
            month_from = 1
        if month_to is None:
            month_to = 12
        if day_from is None:
            day_from = 1
        if day_to is None:
            weekday, day_to = calendar.monthrange(year_to, month_to)
        if time_unit == "year":
            date_from = datetime(year_from, 1, 1, 0, 0, 0)
            date_to = datetime(year_to + 1, 1, 1, 0, 0, 0)
        elif time_unit == "month":
            date_from = datetime(year_from, month_from, 1, 0, 0, 0)

            if month_to == 12:
                year_to += 1
                month_to = 1
            date_to = datetime(year_to, month_to, 1, 0, 0, 0)
        elif time_unit == "day":
            date_from = datetime(year_from, month_from, day_from, 0, 0, 0)
            date_to = datetime(year_to, month_to, day_to, 0, 0, 0) + timedelta(days=1)
        else:
            raise TypeError
    except ValueError:
        raise
    date_from = date_from.strftime("%Y-%m-%dT%H:%M:%SZ")
    date_to = date_to.strftime("%Y-%m-%dT%H:%M:%SZ")
    return (date_from,date_to)

def get_commit_in_range(date_from,date_to,repo_name,owner_name):
    param = {"per_page":1, "since":date_from, "until":date_to} # 按时间获取请求的参数
    #获取commit数据
    commit_url = 'https://api.github.com/repos/' + owner_name+'/'+repo_name + '/commits'
    try:
        commit_request = requests.get(url=commit_url, headers=headers, timeout=5, params=param)
    except requests.exceptions.ReadTimeout:
        raise
    if not commit_request.ok:
        raise requests.exceptions.HTTPError
    commit_info = json.loads(commit_request.content)
    if len(commit_request.links) == 0: # 字典为空，返回值为{}，只有一页
        commit_count = len(commit_info)  # 应为1
    else: # 大于一页，获取页数
        last_str = commit_request.links['last']['url']
        # per_page = int(re.search('per_page=[0-9]+',last_str).group()[9:])
        last_page = int(re.search('[^a-z_]page=[0-9]+',last_str).group()[6:])
        # # 请求最后一个page
        # try:
        #     last_request = requests.get(url=commit_url+"?page="+str(last_page), headers=headers, timeout=5, params=param)
        # except requests.exceptions.ReadTimeout:
        #     raise
        # if not last_request.ok:
        #     raise requests.exceptions.HTTPError
        # last_info = json.loads(last_request.content)
        # commit_count = len(last_info)
        # commit_count += per_page * (last_page-1)
        commit_count = last_page
    return commit_count