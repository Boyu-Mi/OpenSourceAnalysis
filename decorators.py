from functools import wraps
import requests
from flask import request
import json
from model import *

headers = {}
try:
    with open('token', 'r') as token_file:  # 本地有token文件，就用token，没有token就直接查询
        token = token_file.readline()
        headers = {
            "Authorization": token
        }
except FileNotFoundError:
    pass

# 定义登录装饰器，判断用户是否登录
def decorator_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 用url传参不可能没有用户名，省去这步
        # if (user_name is None) or (user_name == ""):  # 没输入用户名
        #     return {
        #                "success": False,
        #                "message": "No user name!"
        #            }, 404
        # 用户名存在
        user_url = "https://api.github.com/users/" + args[0]
        try:
            user_request = requests.get(url=user_url, headers=headers, timeout=5)
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
        kwargs["data"] = json.loads(user_request.content)
        return func(*args, **kwargs)

    return wrapper


def decorator_repo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        url = data.get('url')
        url = url.strip('/')
        if url is None:
            return {
                       "success": False,
                       "message": "No url!"
                   }, 404
        # process the url
        u_list = url.split('/')
        repo_name = u_list[-1]
        owner_name = u_list[-2]
        if 'github.com' not in u_list:
            return {
                       "success": False,
                       "message": "Invalid github repo ink!"
                   }, 404
        repo_url = 'https://api.github.com/repos/' + owner_name + '/' + repo_name
        try:
            repo_request = requests.get(url=repo_url, headers=headers, timeout=5)
        except requests.exceptions.ReadTimeout:
            return {
                       "success": False,
                       "message": "Timeout!"
                   }, 404
        if not repo_request.ok:
            return {
                    "success": False,
                    "message": "Fail to get info! The repo may not exist, or there's a network problem"
                }, 404
        kwargs["u_list"] = u_list
        kwargs["data"] = json.loads(repo_request.content)
        return func(*args, **kwargs)

    return wrapper

def decorator_get_repo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        url = data.get('url')
        url = url.strip('/')
        if url is None:
            return {
                       "success": False,
                       "message": "No url!"
                   }, 404
        # process the url
        u_list = url.split('/')
        repo_name = u_list[-1]
        owner_name = u_list[-2]
        if 'github.com' not in u_list:
            return {
                       "success": False,
                       "message": "Invalid github repo ink!"
                   }, 404
        
        kwargs["u_list"] = u_list
        return func(*args, **kwargs)

    return wrapper

def decorator_repo_no_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        u_list = kwargs["u_list"]
        repo_name = u_list[-1]
        owner_name = u_list[-2]
        repo_url = 'https://api.github.com/repos/' + owner_name + '/' + repo_name
        try:
            repo_request = requests.get(url=repo_url, headers=headers, timeout=5)
        except requests.exceptions.ReadTimeout:
            return {
                       "success": False,
                       "message": "Timeout!"
                   }, 404
        if not repo_request.ok:
            return {
                    "success": False,
                    "message": "Fail to get info! The repo may not exist, or there's a network problem"
                }, 404
        kwargs["data"] = json.loads(repo_request.content)
        return func(*args, **kwargs)

    return wrapper

def decorator_commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        repo_url = 'https://api.github.com/repos/' + args[1] + '/' + args[0] + '/commits'
        try:
            repo_request = requests.get(url=repo_url, headers=headers, params=args[2], timeout=5)
        except requests.exceptions.ReadTimeout:
            return {}, False
        if not repo_request.ok:
            return {}, False
        kwargs["data"] = json.loads(repo_request.content)
        return func(*args, **kwargs)

    return wrapper

def decorator_stargazers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        repo_url = 'https://api.github.com/repos/' + args[1]+'/'+args[0]+'/stargazers'
        try:
            repo_request = requests.get(url=repo_url, headers=headers, params=args[2],timeout=5)
        except requests.exceptions.ReadTimeout:
            return ({},False)
        if not repo_request.ok:
            return ({},False)
        kwargs["data"] = json.loads(repo_request.content)
        return func(*args, **kwargs)
    return wrapper

def decorator_issues(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        repo_url = 'https://api.github.com/repos/' + args[1]+'/'+args[0]+'/issues'
        try:
            repo_request = requests.get(url=repo_url, headers=headers, params=args[2],timeout=5)
        except requests.exceptions.ReadTimeout:
            return ({},False)
        if not repo_request.ok:
            return ({},False)
        kwargs["data"] = json.loads(repo_request.content)
        return func(*args, **kwargs)
    return wrapper


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
            result = db.session.query(Commiter_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Commiter_company.count.desc()).all()
            result_all.append(result)
            if len(result)==0:
                return {
                        "success": False,
                        "message": "The repo has no infomation in database! Please update infomation first."
                    }, 404
            if type == "commits":
                kwargs["result"] = result

            result = db.session.query(Stargazer_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Stargazer_company.count.desc()).all()
            result_all.append(result)
            if len(result)==0:
                return {
                        "success": False,
                        "message": "The repo has no infomation in database! Please update infomation first."
                    }, 404
            if type == "stargazers":
                kwargs["result"] = result

            result = db.session.query(Issue_company).filter_by(repo_name=repo_name,owner_name=owner_name).order_by(Issue_company.count.desc()).all()
            result_all.append(result)
            if len(result)==0:
                return {
                        "success": False,
                        "message": "The repo has no infomation in database! Please update infomation first."
                    }, 404
            if type == "issues":
                kwargs["result"] = result
            
            if type == "all":
                kwargs["result"] = result_all
            return func(*args, **kwargs)
        return wrapper
    return decorator_company_inner
