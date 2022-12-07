import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
db = SQLAlchemy()


class Repos(db.Model):
    id = sa.Column(sa.Integer,
                   primary_key=True,
                   nullable=False)
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    owner_name = sa.Column(sa.String(128), nullable=False, default='')
    about = sa.Column(sa.String(128), nullable=False, default='')
    link = sa.Column(sa.String(128), nullable=False, default='')
    time = sa.Column(sa.DateTime)

class Contributors(db.Model):
    # id = sa.Column(sa.Integer,
    #                primary_key=True,
    #                nullable=False)
    owner_name = sa.Column(sa.String(128),primary_key=True, nullable=False, default='')
    repo_name = sa.Column(sa.String(128),primary_key=True, nullable=False, default='')
    con_name = sa.Column(sa.String(128),primary_key=True, nullable=False, default='')
    con_num = sa.Column(sa.Integer)


class Commits(db.Model):
    id = sa.Column(sa.String(40),
                   primary_key=True,
                   nullable=False)
    owner_name = sa.Column(sa.String(128), nullable=False, default='')
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    con_name = sa.Column(sa.String(128), nullable=False, default='')


class date01(db.Model):
    id = sa.Column(sa.String(40),
                   primary_key=True,
                   nullable=False)
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    date_newest = sa.Column(sa.DateTime)
    date_local = sa.Column(sa.DateTime)  # 目前还不知道自动设置更新时间的方法
    date_lasttime = sa.Column(sa.DateTime)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True,
                   nullable=False)
    user_type = sa.Column(sa.String(50), nullable=False, default='')
    user_name = sa.Column(sa.String(128), nullable=False, default='')
    company = sa.Column(sa.String(128), nullable=True, default='')
    avatar_url = sa.Column(sa.String(128), nullable=True, default='')
    user_url = sa.Column(sa.String(128), nullable=True, default='')
    created_at = sa.Column(sa.DateTime)
    updated_at = sa.Column(sa.DateTime)
    follower_number = sa.Column(sa.Integer, nullable=False, default=0)
    public_repo_number = sa.Column(sa.Integer, nullable=False, default=0)
    time = sa.Column(sa.DateTime)


class Commit_count(db.Model):
    repo_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='')  # 联合主键
    owner_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='')  # 联合主键
    timeline = sa.Column(sa.DateTime, primary_key=True)  # 联合主键
    commit_count = sa.Column(sa.Integer, nullable=False, default=0)  # 该日子下的commit数
    time = sa.Column(sa.DateTime)  # 数据库更新时间

class Issue(db.Model):
    repo_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='')  # 联合主键
    owner_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='')  # 联合主键
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    title = sa.Column(sa.Text, nullable=False, default='')
    body = sa.Column(sa.Text, nullable=False, default='')
    
class Commiter_company(db.Model):
    repo_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    owner_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    company = sa.Column(sa.String(128), primary_key=True) #联合主键
    count = sa.Column(sa.Integer, nullable=False, default=0) #该company人数
    time = sa.Column(sa.DateTime) #数据库更新时间

class Stargazer_company(db.Model):
    repo_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    owner_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    company = sa.Column(sa.String(128), primary_key=True) #联合主键
    count = sa.Column(sa.Integer, nullable=False, default=0) #该company人数
    time = sa.Column(sa.DateTime) #数据库更新时间

class Issue_company(db.Model):
    repo_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    owner_name = sa.Column(sa.String(128), primary_key=True, nullable=False, default='') #联合主键
    company = sa.Column(sa.String(128), primary_key=True) #联合主键
    count = sa.Column(sa.Integer, nullable=False, default=0) #该company人数
    time = sa.Column(sa.DateTime) #数据库更新时间
