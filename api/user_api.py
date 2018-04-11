#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/4/11
Desc    :   
"""
import common
from flask import jsonify
from app import application
from models import User
from schema import UserSchema


def register_user_api():
    @application.route('/api/random_sort_user')
    def random_sort_users():
        first_user = User.query.first()
        data, errors = UserSchema().dump(first_user)
        return jsonify({
            "first_user": data
        })
