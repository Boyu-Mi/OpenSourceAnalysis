from flask import Blueprint,request
import requests
import json
from datetime import datetime, timedelta
from model import *
import time
from decorators import decorator_repo,decorator_commit

blueprint = Blueprint("update", __name__)

headers = {}

    
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
    page=1
    param = {"per_page":100,"page":page}
    dict={}
    data = get_commit_info(repo_name,owner_name,param,dict)
    if data[1] == False:
        return False
    dict = data[0]
    while(data is not None and page <=10): # 只能查看最近1000条，若要更改请改page参数
        page += 1
        param = {"per_page":100,"page":page}
        data = get_commit_info(repo_name,owner_name,param,dict)
        if data[1] == False:
            return False
        dict = data[0]

    print(dict)

    time = datetime.now()
    for key,value in dict.items():
        # 存储信息到数据库
        db.session.merge(
            Commit_count(repo_name=repo_name,owner_name=owner_name,timeline=key,commit_count=value, time=time)
        )
        db.session.commit()
    return