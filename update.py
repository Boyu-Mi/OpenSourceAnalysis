from flask import Blueprint,request
import requests
import json
from datetime import datetime, timedelta
from model import *
import time
from decorators import decorator_repo,decorator_commit,decorator_stargazers,decorator_issues
import view.user
from view.contributor import updateContributors

blueprint = Blueprint("update", __name__)

    
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

    dic = updateContributors()[0]
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
def get_commit_info(repo,owner,param,dict,data = {}):
    for i in range(0,len(data)):
        c_time = data[i]["commit"]["author"]["date"]
        c_time = c_time[0:10]
        if c_time in dict.keys():
            dict[c_time] += 1
        else:
            dict[c_time] = 1
    return dict,True #最后一个返回值表示成功与否

def update_commit_by_time(repo_name,owner_name,data = {}):
    page=0
    param = {"per_page":100,"page":page}
    dict={}
    data = {}
    while(data is not None and page <=5): # 只能查看最近500条，若要更改请改page参数
        page += 1
        param = {"per_page":100,"page":page}
        data = get_commit_info(repo_name,owner_name,param,dict)
        if data[1] == False:
            return False
        dict = data[0]

    time = datetime.now()
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