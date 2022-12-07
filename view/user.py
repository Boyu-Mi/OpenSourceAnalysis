from flask import Blueprint, request

from datetime import datetime
from model import *
from decorators import decorator_user
import re

blueprint = Blueprint("user", __name__)


# 获取某个用户的信息，包括organization，company(user只用单个请求，比较快，就不存数据库了)
@blueprint.route('/get_user/<name>/', methods=['GET', 'POST'])
def user(name):
    result = db.session.query(User).filter_by(user_name=name).first()
    if result is None or len(result)==0:
        return update_user(name)
    ret = {}
    user_name = name
    ret = {"success": True, "message": "success!", "user_name": user_name, "id": result.id,
           "avatar_url": result.avatar_url, "user_url": result.user_url, "user_type": result.user_type,
           "company": result.company, "public_repo_number": result.public_repo_number,
           "follower_number": result.follower_number, "created_at": result.created_at, "updated_at": result.updated_at,
           "time": result.time}
    return ret, 200


@decorator_user
def update_user(name, data=None):
    if data is None:
        data = {}
    user_name = name
    user_info = data
    ret = {"success": True, "message": "success!", "user_name": user_name}
    ret["id"] = user_info["id"]
    ret["avatar_url"] = user_info["avatar_url"]
    ret["user_url"] = user_info["html_url"]
    ret["user_type"] = user_info["type"]  # Organization,User等
    company = user_info["company"]
    if company is None:
        company = ""
    company = re.search("(\\w| )+",company)
    if company is None:
        company = ""
    else:
        company = company.group()
    company = re.sub("\\s*$","",company) #去掉左右两侧空格
    company = re.sub("^\\s*","",company)
    company = company.lower()
    ret["company"] = company
    ret["public_repo_number"] = user_info["public_repos"]
    ret["follower_number"] = user_info["followers"]
    ret["created_at"] = user_info["created_at"][0:10] + ' ' + user_info["created_at"][11:19]
    ret["updated_at"] = user_info["updated_at"][0:10] + ' ' + user_info["updated_at"][11:19]
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
             user_name=user_name, company=ret["company"],
             avatar_url=ret["avatar_url"], user_url=ret["user_url"], created_at=date_c, updated_at=date_u,
             follower_number=ret["follower_number"], public_repo_number=ret["public_repo_number"], time=time)
    )
    db.session.commit()
    return ret, 200
