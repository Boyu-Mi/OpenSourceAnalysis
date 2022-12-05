from flask import Blueprint,request
from datetime import datetime, timedelta

from decorators import decorator_company

blueprint = Blueprint("company", __name__)


@blueprint.route('/get_company_all/', methods=['GET', 'POST'])
@decorator_company("all")
def get_company_all(u_list=None, result=None):
    dic = {}
    timestr = result[0][0].time.strftime("%Y-%m-%d %H:%M:%S")
    for ls in result:
        for item in ls:
            if item.company in dic.values():
                dic[item.company] += item.count
            else:
                dic[item.company] = item.count
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    dic= dict(sorted(dic.items(), key=lambda d:d[1], reverse = True))
    company = list(dic.keys())
    count = list(dic.values())
    ret = {}
    ret["time"] = timestr
    res = {"contributer" : company[0:10], "data" : count[0:10]} # 只取最高的10家公司
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = repo_name
    ret["owner_name"] = owner_name
    ret["content"] = res
    return ret, 200


@blueprint.route('/get_company_commits/', methods=['GET', 'POST'])
@decorator_company("commits")
def get_company_commiters(u_list=None, result=None):
    company = []
    count = []
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
    ret = {}
    ret["time"] = timestr
    for item in result:
        company.append(item.company)
        count.append(item.count)
    
    res = {"contributer" : company[0:10], "data" : count[0:10]}
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = repo_name
    ret["owner_name"] = owner_name
    ret["content"] = res
    return ret, 200

@blueprint.route('/get_company_stargazers/', methods=['GET', 'POST'])
@decorator_company("stargazers")
def get_company_stargazers(u_list=None, result=None):
    company = []
    count = []
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
    ret = {}
    ret["time"] = timestr
    for item in result:
        company.append(item.company)
        count.append(item.count)
    
    res = {"contributer" : company[0:10], "data" : count[0:10]}
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = repo_name
    ret["owner_name"] = owner_name
    ret["content"] = res
    return ret, 200

@blueprint.route('/get_company_issues/', methods=['GET', 'POST'])
@decorator_company("issues")
def get_company_issues(u_list=None, result=None):
    company = []
    count = []
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
    ret = {}
    ret["time"] = timestr
    for item in result:
        company.append(item.company)
        count.append(item.count)
    
    res = {"contributer" : company[0:10], "data" : count[0:10]}
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = repo_name
    ret["owner_name"] = owner_name
    ret["content"] = res
    return ret, 200