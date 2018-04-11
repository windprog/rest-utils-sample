#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/3/14
Desc    :   
"""
import common
from flask import request
from rest_utils.schema import default_create, default_update
from rest_utils.exception import PermissionDenied

from api.util import is_supervuser


def post_update(instance, data):
    """
    权限例子
    本例说明：
        只有超级管理员才可以修改文章
    :return:
    """
    if getattr(request, 'user'):
        if is_supervuser():
            # 超级管理员：允许修改文章
            return default_update(instance, data)
    raise PermissionDenied


def post_create(model, data):
    if not hasattr(request, "user"):
        # 未登录用户无法创建文章
        raise PermissionDenied
    return default_create(model, data)
