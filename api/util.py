#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   zzn1889@corp.netease.com
Date    :   16/10/18
Desc    :   
"""
import re
from flask import request, abort
import httplib


def url_quote(s):
    s = re.sub("[^a-zA-Z0-9ßäüö.]", " ", s, flags=re.U).strip(' -').lower()  # stripe " " and "-" char
    s = re.sub("\s", "-", s, flags=re.U)
    s = re.sub("-+", "-", s, flags=re.U)
    return s


def is_supervuser():
    try:
        return getattr(request, 'user', None) and request.user.is_superuser
    except RuntimeError:
        # 没有进入flask request
        return True


def get_value_from_header(name):
    value = request.cookies.get('AUTH_' + name.upper())
    if value is not None:
        return value
    value = request.headers.get('X-Auth-' + name.title())
    return value


def process_auth(*args, **kwargs):
    """
    粗略的登陆验证
    :return:
    """
    from models import User

    username = get_value_from_header('user')
    if username:
        user = User.query_.filter(User.username == username).first()
        if user:
            # 登陆成功
            request.user = user
        else:
            # 登陆错误
            abort(httplib.FORBIDDEN)
    else:
        # 游客浏览
        request.user = None
