from flask import Blueprint,request
from datetime import datetime, timedelta
from model import *
from decorators import decorator_get_repo,decorator_repo_no_request

blueprint = Blueprint("get_repo", __name__)

@blueprint.route('/get_repo/', methods=['GET', 'POST'])
@decorator_get_repo
def get_repo(u_list=None):
    db.create_all()
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    
    result = db.session.query(Repos).filter_by(repo_name=repo_name, owner_name=owner_name).first()
    if result is None:
        return new_repo(u_list=u_list)
    ret = {"success": True, "message": "success!", "time": result.time}
    res = {
        "id": result.id,
        "name": repo_name,
        "owner": owner_name,
        "about": result.about,
        "link": result.link,
        "stargazers_count": result.stargazers_count,
        "forks_count" :result.forks_count,
        "watchers_count": result.watchers_count
    }
    ret["content"] = res
    return ret, 200


@decorator_repo_no_request
def new_repo(u_list=None,data=None):
    repo_name = u_list[-1]
    owner_name = u_list[-2]

    time = datetime.now()
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")

    ret = {"success": True, "message": "success!", "time": timestr}
    res = {
        "id": data["id"],
        "name": repo_name,
        "owner": owner_name,
        "about": data["description"],
        "link": data["html_url"],
        "stargazers_count" : data['stargazers_count'],  # number of star
        "forks_count" : data['forks_count'],
        "watchers_count" : data['watchers_count']
    }

    
    # 存储信息到数据库
    db.session.merge(
        Repos(id=res["id"], repo_name=repo_name, owner_name=owner_name, about=data["description"],link=data["html_url"],
        time=time,stargazers_count=data['stargazers_count'], forks_count=data['forks_count'],watchers_count=data['watchers_count'])
    )
    db.session.commit()
    ret["content"] = res
    return ret, 200
