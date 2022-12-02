from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin  # 处理跨域
import requests
import json
import config
from datetime import datetime, timedelta
import calendar
import os
from sqlalchemy.sql import and_, or_
from flask_cors import CORS

from model import db
from model import *
import re
import cloud.cloud
import random
import time

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)  # 支持跨域

# 给仓库链接返回相关信息
@app.route('/get_repo/', methods=['GET', 'POST'])
def get_repo():
    data = request.json
    print(data)
    res = {
            "id": config.num,
            "name": "pytorch" + str(config.num),
            "about": "About Tensors and Dynamic neural networks in Python with strong GPU acceleration",
            "link": "https://github.com/pytorch/pytorch" + str(config.num)
            }
    config.num += 1
    if(config.num >= 9):
        config.num = 1
    return ({"content" : res}, 200)


@app.route('/get_commit/', methods=['GET', 'POST'])
def get_commit():

# {
#     "url" : STRING
# }
    """
    :return:
    """
    data = request.json
    print(data)
    res = ({'success': True, 'message': 'success!', 'target': 'pytorch/pytorch', 
            'id': 65600975, 'url': 'https://github.com/pytorch/pytorch', 
            'owner': 'pytorch', 'avatar_url': 'https://avatars.githubusercontent.com/u/21003710?v=4', 
            'html_url': 'https://github.com/pytorch', 
            'description': 'Tensors and Dynamic neural networks in Python with strong GPU acceleration', 
            'topics': ['autograd', 'deep-learning', 'gpu', 'machine-learning', 'neural-network', 
            'numpy', 'python', 'tensor'], 'stargazers_count': 60661, 'created_at': '2016-08-13T05:26:41Z', 
            'commit_users': [{'user': 'awgu', 'url': 'https://github.com/awgu', 
            'a_url': 'https://avatars.githubusercontent.com/u/31054793?v=4'}, 
            {'user': 'pytorchmergebot', 'url': 'https://github.com/pytorchmergebot', 
            'a_url': 'https://avatars.githubusercontent.com/u/97764156?v=4'}, 
            {'user': 'wz337', 'url': 'https://github.com/wz337', 'a_url': 'https://avatars.githubusercontent.com/u/31293777?v=4'}, 
            {'user': 'pearu', 'url': 'https://github.com/pearu', 'a_url': 'https://avatars.githubusercontent.com/u/402156?v=4'}, 
            {'user': 'jerryzh168', 'url': 'https://github.com/jerryzh168', 
            'a_url': 'https://avatars.githubusercontent.com/u/4958441?v=4'},
            {'user': 'ezyang', 'url': 'https://github.com/ezyang', 
            'a_url': 'https://avatars.githubusercontent.com/u/13564?v=4'}, 
            {'user': 'wanchaol', 'url': 'https://github.com/wanchaol', 
            'a_url': 'https://avatars.githubusercontent.com/u/9443650?v=4'}, 
            {'user': 'r-barnes', 'url': 'https://github.com/r-barnes', 
            'a_url': 'https://avatars.githubusercontent.com/u/3118036?v=4'}, 
            {'user': 'mingfeima', 'url': 'https://github.com/mingfeima', 
            'a_url': 'https://avatars.githubusercontent.com/u/20233731?v=4'}, 
            {'user': 'janeyx99', 'url': 'https://github.com/janeyx99', 
            'a_url': 'https://avatars.githubusercontent.com/u/31798555?v=4'}], 
            'date_newest': "今天", 'forks_count': 16894, 'watchers_count': 60661}, 200)
    
    return res

@app.route('/get_company_commits', methods=['GET', 'POST'])
def get_company_commits():

# {
#     "url" : STRING
# }

    """
    返回仓库的贡献者 ---------------------  这个返回结果是要排序过吗
    [
        {value : INT, name : STRING}
        ...
    ]
    """
    data = request.json
    print(data)
    con = []
    data = []

    for i in range (10):
        con.append("公司" + str(i))
        data.append(str(random.randint(50*i, 50*i + 50)))

    res = {
        "contributer" : con,
        "data" : data
    }
    print(res)

    return ({"content" : res}, 200)

@app.route('/get_contributors/all', methods=['GET', 'POST'])
def get_contributors():

# {
#     "url" : STRING
# }

    """
    返回仓库的贡献者
    [
        {value : INT, name : STRING}
        ...
    ]
    """
    data = request.json
    print(data)
    res = [
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))}
    ]

    return ({"content" : res}, 200)


@app.route('/get_contributors/core', methods=['GET', 'POST'])
def get_core_contributors():

# {
#     "url" : STRING
# }
    """
    返回仓库的核心贡献者

    """
    data = request.json
    print(data)
    res = [
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))},
        {"value" : random.randint(1, 100000), "name" : str(random.randint(1000, 1000000))}
    ]
    return ({"content": res}, 200)
    # 其他东西随便加


@app.route('/get_user/<id>', methods=["GET"])
def get_user(id):
    # 获取某个用户的信息，包括organization，company
    id = int(id)
    ret = {
        "avatar_url": "",
        "company" : "浙江大学" + str(random.randint(0, 99999)),
        "created_at": "2021-08-25T12:43:21Z",
        "follower_number": random.randint(0, 99999),
        "id": id,
        "name" : "hzzz" + str(random.randint(0, 99999)) + "号",
        "message": "success!",
        "public_repo_number": random.randint(0, 999999),
        "success": True,
        "updated_at": "2022-11-04 14:40:23",
        "user_name": "用户名",
        "user_type": "用户类型",
        "user_url": "用户页url",
        "time": "2022-11-10 14:40:23"
    }

    return ret, 200




@app.route('/get_commit_by_time/', methods=['GET', 'POST'])
def get_commit_by_time():

# {
#     "url" : STRING
# }

    data = request.json
    print(data)

    timeline = []
    ydata = []
    for i in range(10):
        for j in range(12):
            for k in range(30):
                timeline.append(str(2010 + i) + "/" + str(1+j) + "/" + str(1 + k))
                ydata.append(random.randint(10, 1000))
    res = {"timeline" : timeline, "ydata" : ydata}

    return ({"content" : res}, 200)

# 现在返回所有历史时间
# timeline: ['2022/10/1', '2022/10/2', '2022/10/3', 
#     '2022/10/4', '2022/10/5', '2022/10/6', '2022/10/7',
#     '2021/10/1', '2021/10/2', '2021/10/3', 
#     '2021/10/4', '2021/10/5', '2021/10/6', '2021/10/7',
#     '2022/10/1', '2022/10/2', '2022/10/3', 
#     '2022/10/4', '2022/10/5', '2022/10/6', '2022/10/7',
#     '2021/10/1', '2021/10/2', '2021/10/3', 
#     '2021/10/4', '2021/10/5', '2021/10/6', '2021/10/7',
#     '2022/10/1', '2022/10/2', '2022/10/3', 
#     '2022/10/4', '2022/10/5', '2022/10/6', '2022/10/7',
#     '2021/10/1', '2021/10/2', '2021/10/3', 
#     '2021/10/4', '2021/10/5', '2021/10/6', '2021/10/7'
#   ],
#     ydata: [820, 932, 901, 934, 1290, 1330, 1320,
#       820, 932, 901, 934, 1290, 1330, 1320,
#       820, 932, 901, 934, 1290, 1330, 1320,
#       820, 932, 901, 934, 1290, 1330, 1320,
#       820, 932, 901, 934, 1290, 1330, 1320,
#       820, 932, 901, 934, 1290, 1330, 1320
#     ]

# 这里缺个转换
def convert_url(url):
    array = url.split("A")
    new_url = ""
    for i in range(len(array) - 1):
        new_url += chr(int(array[i+1]))
    return new_url

@app.route("/cloud/<url>", methods=["GET"])
def get_cloud_image(url):
    new_url = convert_url(url)
    print( "--- Cloud url: " + new_url + "---")

    text = (open('cloud\\test_' + str(random.randint(0, 9)) + ".txt", "r", encoding='utf-8')).read()
    # 单纯获取测试用的字符串，直接make然后返回就可以了
    res = cloud.cloud.make_cloud_img(text, 3)
    print(res[1])
    return cloud.cloud.im_2_b64(res[0])

@app.route("/update_repo", methods=["POST"])
def get_update():
    data = request.json
    print(data)
    update_repo_with_url(data.get("url"))
    return {"success" : True}


def update_repo_with_url(url):
    time.sleep(15)
    return

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
