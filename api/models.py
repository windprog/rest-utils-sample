#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   16/10/17
Desc    :
"""
import datetime
from flask_sqlalchemy import SQLAlchemy

# MYSQL配置
DB_URL = "mysql://root:windpro@localhost/sample_blog?charset=utf8"
# SQLITE配置
# DB_URL = 'sqlite:////tmp/test.db'

db = SQLAlchemy()
Base = db.Model

# 关联表
user_groups = db.Table(
    'user_groups', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)
user_follower = db.Table(
    'user_follower', Base.metadata,
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


# 模型
class User(Base):
    '''
    博客用户表
    '''
    __tablename__ = 'users'  # 表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(32), unique=True)  # 用户名唯一
    password = db.Column('password', db.Unicode(128))
    email = db.Column(db.Unicode(128))
    phone = db.Column(db.CHAR(11))

    # 绑定一对一关系
    # 用户验证状态
    validation = db.relationship(
        'UserValidation',
        uselist=False,
        backref=db.backref('user')
    )

    # 绑定一对多关系
    # 用户文章列表
    posts = db.relationship(
        'Post',
        backref=db.backref('user')
    )

    # 使用 secondary 绑定多对多关系
    # 用户组列表
    groups = db.relationship(
        'Group',
        secondary=user_groups,
        backref=db.backref('users')  # 组内的用户
    )

    # 使用primaryjoin和secondaryjoin实现关联自身的关系
    # 用粉丝和关注列表，多对多关系
    followed = db.relationship(  # 粉丝列表
        'User',
        secondary=user_follower,
        primaryjoin=(user_follower.c.follower_id == id),
        secondaryjoin=(user_follower.c.followed_id == id),
        backref=db.backref(
            'followers',  # 关注的用户列表
            lazy='dynamic'
        ),
        lazy='dynamic'
    )


class UserValidation(Base):
    """
    用户验证状态
    """
    __tablename__ = 'user_validation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    passed_email = db.Column(db.Boolean, default=False)
    passed_phone = db.Column(db.Boolean, default=False)


class Group(Base):
    '''
    用户组
    本例包含了：
        1、多字段的唯一约束
        2、组合索引
    '''
    __tablename__ = 'groups'
    __table_args__ = (
        db.UniqueConstraint(
            'name', 'permission_type',
            name='groups_unique_name_permission_type'
        ),  # 唯一约束（这个属于胡来，博客模型里不存在多字段同时唯一）
        db.Index(
            'groups_index_name_permission_type',
            'name', 'permission_type',
        ),  # 联合索引（组合索引）
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(128))
    permission_type = db.Column(
        db.Enum('superuser', 'committer', 'normal', 'deny'),
        default='normal',
    )


class Post(db.Model):
    """
    文章
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(80), nullable=False, unique=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
