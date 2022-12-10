import json
import os
import random
from datetime import datetime
from view.issue import textForCloud

import requests
from flask import Flask, request
from flask_cors import CORS
import config
import view.view, view.commit, view.contributor, view.issue
from model import *
import update, view.user, view.commit_by_time as commit_by_time, view.company, view.get_repo
import cloud.cloud
from flask_migrate import Migrate

app = Flask(__name__)


# 注册蓝图
app.register_blueprint(update.blueprint, url_prefix='/')
app.register_blueprint(view.user.blueprint, url_prefix='/')
app.register_blueprint(commit_by_time.blueprint, url_prefix='/')
app.register_blueprint(view.issue.blueprint, url_prefix='/')
app.register_blueprint(view.commit.blueprint, url_prefix='/')
app.register_blueprint(view.contributor.blueprint, url_prefix='/')
app.register_blueprint(view.company.blueprint,url_prefix='/')
app.register_blueprint(view.get_repo.blueprint,url_prefix='/')

basedir = os.path.abspath(app.root_path)
app.config.from_object(config)  # 读取配置
db.init_app(app)
cors = CORS(app, supports_credentials=True)  # 支持跨域

headers = {}
try:
    with open('token', 'r') as token_file:  # 本地有token文件，就用token，没有token就直接查询
        token = token_file.readline()
        headers = {
            "Authorization": token
        }
except FileNotFoundError:
    pass

# 初始化 migrate
# 两个参数一个是 Flask 的 app，一个是数据库 db
Migrate(app, db)


# 这里缺个转换
def convert_url(url):
    array = url.split("A")
    new_url = ""
    for i in range(len(array) - 1):
        new_url += chr(int(array[i + 1]))
    return new_url


@app.route("/cloud/<num>/<path:url>", methods=["GET","POST"])
def get_cloud_image(num,url):
    new_url = convert_url(num)
    print( "--- Cloud url: " + new_url + "---")
    text = textForCloud(url)
    # 单纯获取测试用的字符串，直接make然后返回就可以了
    res = cloud.cloud.make_cloud_img(text, 2)
    # print(res[1])
    return cloud.cloud.im_2_b64(res[0])


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
