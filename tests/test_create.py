#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/3/14
Desc    :   
"""
import common
from json import dumps, loads
from api.app import application

client = application.test_client()


def test_func():
    """
    创建用户
    :param req: 跟requests库的用法一致
    :return:
    """
    res = client.put('/api/users', headers={
        "Content-Type": 'application/json'
    }, data=dumps({
        "name": "windprozhao",
        'posts': [
            {
                'title': 'Hello Python!',
                'body': 'Python is pretty cool',
            },
            {
                'title': 'Snakes',
                'body': 'Ssssssss',
            },
        ],
        "groups": [
            {
                "name": "admin",
                "permission_type": "superuser",
            },
            {
                "name": "you ke",
                "permission_type": "normal",
            },

        ]
    }))
    assert res.status_code in [201, 200]  # 创建分类成功
    assert loads(res.data)['name'] == 'windprozhao'

    # 检查创建分类
    addr = client.get('/api/users/@windprozhao')
    assert 'name' in loads(addr.data)

    # 检查文章创建
    posts = client.get('/api/posts?title=Snakes')
    assert len(loads(posts.data)["items"]) == 1


def test_groups():
    """
    检查组创建成功，并检查自定义 /api/groups 字段
    :param req: 跟requests库的用法一致
    :return:
    """
    res = client.put('/api/users', headers={
        "Content-Type": 'application/json'
    }, data=dumps({
        "name": "windprozhao",
        'posts': [
            {
                'title': 'Hello Python!',
                'body': 'Python is pretty cool',
            },
            {
                'title': 'Snakes',
                'body': 'Ssssssss',
            },
        ],
        "groups": [
            {
                "name": "admin",
                "permission_type": "superuser",
            },
            {
                "name": "you ke",
                "permission_type": "normal",
            },

        ]
    }))
    assert res.status_code in [201, 200]  # 创建分类成功
    assert loads(res.data)['name'] == 'windprozhao'
    # 检查分组
    groups = client.get('/api/groups')
    assert len(loads(groups.data)["items"]) == 2
    frist_group = loads(groups.data)["items"][0]
    # 检查动态添加的字段
    assert "sort" in frist_group
    assert frist_group["sort"] < 10


def test_users():
    """
    检查组创建成功，并检查自定义 /api/users/@windprozhao/groups 字段
    :param req: 跟requests库的用法一致
    :return:
    """
    res = client.put('/api/users', headers={
        "Content-Type": 'application/json'
    }, data=dumps({
        "name": "windprozhao",
        'posts': [
            {
                'title': 'Hello Python!',
                'body': 'Python is pretty cool',
            },
            {
                'title': 'Snakes',
                'body': 'Ssssssss',
            },
        ],
        "groups": [
            {
                "name": "admin",
                "permission_type": "superuser",
            },
            {
                "name": "you ke",
                "permission_type": "normal",
            },

        ]
    }))
    assert res.status_code in [201, 200]  # 创建分类成功
    assert loads(res.data)['name'] == 'windprozhao'
    # 检查分组
    user = client.get('/api/users/@windprozhao?_expand=1')
    user_groups = loads(user.data)["groups"]
    assert len(user_groups) == 2
    frist_group = user_groups[0]
    # 检查动态添加的字段
    assert "user_sort" in frist_group
    assert 10 <= frist_group["user_sort"] < 20
    assert "sort" not in frist_group
