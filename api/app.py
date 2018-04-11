#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   15/10/30
Desc    :   
"""
import common
from flask import Flask
from rest_utils import APIManager

import models
from schema import GroupSchema, UserSchema
from util import process_auth
from filter import post_update, post_create

# API_URI为博客系统的api url_prefix
# 因为线上系统一般要做api版本管理
API_URI = '/api'


def register_api(app):
    # 登陆验证
    app.before_request(process_auth)
    # 只允许admin用户创建和修改帖子
    api.add(models.Post, methods=['GET', "POST", "PUT"], create=post_create, update=post_update)
    api.add(UserSchema, methods=['GET', "POST", "PUT", "DELETE"], key_field="name")
    # 自定义schema
    api.add(GroupSchema, methods=['GET', "POST", "PUT", "DELETE"])


def create_app():
    # 创建app
    app = Flask(__name__)
    # 配置app
    app.config['SQLALCHEMY_DATABASE_URI'] = models.DB_URL  # 配置数据库
    app.config['SQLALCHEMY_ECHO'] = False  # 是否打印sql语句
    app.secret_key = "secret_key"
    models.db.init_app(app)
    return app


def init_app(app):
    from user_api import register_user_api
    # 注册框架api
    register_api(app)
    # 注册自定义api
    register_user_api()


def create_sql():
    # 创建数据库
    from sqlalchemy import create_engine
    engine = create_engine(models.DB_URL, echo=True)
    models.Base.metadata.drop_all(engine)  # 清空数据库
    models.Base.metadata.create_all(engine)  # 创建数据库
    return engine


application = create_app()
api = APIManager(application, db=models.db)
init_app(application)

if __name__ == '__main__':
    create_sql()
