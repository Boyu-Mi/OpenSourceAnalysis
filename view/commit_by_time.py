from flask import Blueprint,request
from model import *
from update import update_commit_by_time


blueprint = Blueprint("commit_by_time", __name__)

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

@blueprint.route('/get_commit_by_time/', methods=['GET', 'POST'])
def commit_by_time():
    # db.create_all()
    data = request.json
    url = data.get('url')
    url = url.strip('/')
    u_list = url.split('/')
    timeline = []
    commit_count = []
    repo_name = u_list[-1]
    owner_name = u_list[-2]
    result = db.session.query(Commit_count).filter_by(repo_name=repo_name,owner_name=owner_name).all()
    if len(result)==0:
        # return {
        #             "success": False,
        #             "message": "The repo has no infomation in database! Please update infomation first."
        #         }, 404
        update_commit_by_time(repo_name,owner_name)
        result = db.session.query(Commit_count).filter_by(repo_name=repo_name,owner_name=owner_name).all()
    timestr = result[0].time.strftime("%Y-%m-%d %H:%M:%S")
    ret = {}
    ret["time"] = timestr
    for item in result:
        timelinestr = item.timeline.strftime("%Y-%m-%d")
        timeline.append(timelinestr)
        commit_count.append(item.commit_count)
    
    res = {"timeline" : timeline, "ydata" : commit_count}
    ret = {"success": True, "message": "success!"}
    ret["repo_name"] = repo_name
    ret["owner_name"] = owner_name
    ret["content"] = res
    return ret, 200