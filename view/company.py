from flask import Blueprint,request
from functools import wraps
from datetime import datetime, timedelta
from model import *
from update import update_company
# from decorators import decorator_company

blueprint = Blueprint("company", __name__)


def decorator_company(type):
    def decorator_company_inner(func):
        my_type = type
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.json
            url = data.get('url')
            url = url.strip('/')
            u_list = url.split('/')
            repo_name = u_list[-1]
            owner_name = u_list[-2]
            result_all = []
            type = my_type
            
            kwargs["u_list"] = u_list
            result1 = db.session.query(Commiter_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Commiter_company.count.desc()).all()
            result2 = db.session.query(Stargazer_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Stargazer_company.count.desc()).all()
            result3 = db.session.query(Issue_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Issue_company.count.desc()).all()
            
            if len(result1)==0 or len(result2)==0 or len(result3)==0:
                # return {
                #         "success": False,
                #         "message": "The repo has no infomation in database! Please update infomation first."
                #     }, 404
                update_company(repo_name,owner_name)
            
            result = db.session.query(Commiter_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Commiter_company.count.desc()).all()
            result_all.append(result)
            
            if type == "commits":
                kwargs["result"] = result

            result = db.session.query(Stargazer_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Stargazer_company.count.desc()).all()
            result_all.append(result)
            
            #     return {
            #             "success": False,
            #             "message": "The repo has no infomation in database! Please update infomation first."
            #         }, 404
            if type == "stargazers":
                kwargs["result"] = result

            result = db.session.query(Issue_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Issue_company.count.desc()).all()
            result_all.append(result)
            
            #     return {
            #             "success": False,
            #             "message": "The repo has no infomation in database! Please update infomation first."
            #         }, 404
            if type == "issues":
                kwargs["result"] = result
            
            if type == "all":
                kwargs["result"] = result_all
            return func(*args, **kwargs)
        return wrapper
    return decorator_company_inner

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
    ret = {}
    if len(result) == 0:
        res = {"contributer" : ["No commiter or no company"], "data" : [0]}
        ret = {"success": True, "message": "No company info"}
        ret["repo_name"] = repo_name
        ret["owner_name"] = owner_name
        ret["content"] = res
        return ret, 200
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
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
    ret = {}
    if len(result) == 0:
        res = {"contributer" : ["No stargazer or no company"], "data" : [0]}
        ret = {"success": True, "message": "No company info"}
        ret["repo_name"] = repo_name
        ret["owner_name"] = owner_name
        ret["content"] = res
        return ret, 200
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
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
    ret = {}
    if len(result) == 0:
        res = {"contributer" : ["No issue or no company"], "data" : [0]}
        ret = {"success": True, "message": "No company info"}
        ret["repo_name"] = repo_name
        ret["owner_name"] = owner_name
        ret["content"] = res
        return ret, 200
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
    
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
