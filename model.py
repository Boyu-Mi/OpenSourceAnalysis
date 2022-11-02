import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Contributors(db.Model):
    id = sa.Column(sa.Integer, autoincrement=True,
                   primary_key=True,
                   nullable=False)
    owner_name = sa.Column(sa.String(128), nullable=False, default='')
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    con_name = sa.Column(sa.String(128), nullable=False, default='')
    con_num = sa.Column(sa.Integer)


class Commits(db.Model):
    id = sa.Column(sa.Integer, autoincrement=True,
                   primary_key=True,
                   nullable=False)
    owner_name = sa.Column(sa.String(128), nullable=False, default='')
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    con_name = sa.Column(sa.String(128), nullable=False, default='')


class date01(db.Model):
    id = sa.Column(sa.Integer, autoincrement=True,
                   primary_key=True,
                   nullable=False)
    repo_name = sa.Column(sa.String(128), nullable=False, default='')
    date_newest = sa.Column(sa.DateTime)
    date_local = sa.Column(sa.DateTime)  #目前还不知道自动设置更新时间的方法
    date_lasttime = sa.Column(sa.DateTime)
