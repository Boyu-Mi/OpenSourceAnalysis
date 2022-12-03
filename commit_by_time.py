from flask import Blueprint,request
from datetime import datetime, timedelta
from model import *


blueprint = Blueprint("commit_by_time", __name__)

headers = {}

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
    # 返回: total_commit 按时间的commit数, 默认起止年月日，输入允许为空（不传对应参数即可。）
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
        return {
                    "success": False,
                    "message": "The repo has no infomation in database! Please update infomation first."
                }, 404
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

# 暂时用不上这俩函数了
# def get_complete_date(time_unit, year_from, year_to, month_from, month_to, day_from, day_to):
#     try:  # 判断日期合法性
#         # 处理空值
#         if year_from is None:
#             year_from = 2000  # github创建时间2008
#         if year_to is None:
#             year_to = datetime.today().year
#         if month_from is None:
#             month_from = 1
#         if month_to is None:
#             month_to = 12
#         if day_from is None:
#             day_from = 1
#         if day_to is None:
#             weekday, day_to = calendar.monthrange(year_to, month_to)
#         if time_unit == "year":
#             date_from = datetime(year_from, 1, 1, 0, 0, 0)
#             date_to = datetime(year_to + 1, 1, 1, 0, 0, 0)
#         elif time_unit == "month":
#             date_from = datetime(year_from, month_from, 1, 0, 0, 0)

#             if month_to == 12:
#                 year_to += 1
#                 month_to = 1
#             date_to = datetime(year_to, month_to, 1, 0, 0, 0)
#         elif time_unit == "day":
#             date_from = datetime(year_from, month_from, day_from, 0, 0, 0)
#             date_to = datetime(year_to, month_to, day_to, 0, 0, 0) + timedelta(days=1)
#         else:
#             raise TypeError
#     except ValueError:
#         raise
#     date_from = date_from.strftime("%Y-%m-%dT%H:%M:%SZ")
#     date_to = date_to.strftime("%Y-%m-%dT%H:%M:%SZ")
#     return (date_from,date_to)

# def get_commit_in_range(date_from,date_to,u_list):
#     param = {"per_page":1, "since":date_from, "until":date_to} # 按时间获取请求的参数
#     #获取commit数据
#     commit_url = 'https://api.github.com/repos/' + u_list[-2]+'/'+u_list[-1] + '/commits'
#     try:
#         commit_request = requests.get(url=commit_url, headers=headers, timeout=5, params=param)
#     except requests.exceptions.ReadTimeout:
#         raise
#     if not commit_request.ok:
#         raise requests.exceptions.HTTPError
#     commit_info = json.loads(commit_request.content)
#     if len(commit_request.links) == 0: # 字典为空，返回值为{}，只有一页
#         commit_count = len(commit_info)  # 应为1
#     else: # 大于一页，获取页数
#         last_str = commit_request.links['last']['url']
#         # per_page = int(re.search('per_page=[0-9]+',last_str).group()[9:])
#         last_page = int(re.search('[^a-z_]page=[0-9]+',last_str).group()[6:])
#         # # 请求最后一个page
#         # try:
#         #     last_request = requests.get(url=commit_url+"?page="+str(last_page), headers=headers, timeout=5, params=param)
#         # except requests.exceptions.ReadTimeout:
#         #     raise
#         # if not last_request.ok:
#         #     raise requests.exceptions.HTTPError
#         # last_info = json.loads(last_request.content)
#         # commit_count = len(last_info)
#         # commit_count += per_page * (last_page-1)
#         commit_count = last_page
#     return commit_count