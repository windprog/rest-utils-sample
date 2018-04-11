#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/4/11
Desc    :   
"""
import common
import random
from flask import jsonify
from app import application
from models import User
from schema import UserSchema
from rest_utils.utils import get_session


def register_user_api():
    @application.route('/api/query_first_user')
    def query_first_user():
        first_user = User.query.first()
        data, errors = UserSchema().dump(first_user)
        return jsonify({
            "first_user": data
        })

    @application.route('/api/create_random_user')
    def create_random_user():
        session = get_session()
        schema = UserSchema(session=session)
        ins, errors = schema.load({
            "name": "test_user" + str(random.randint(1, 100))
        })
        session.add(ins)
        session.commit()
        return jsonify({
            "random_user": schema.dump(ins).data
        })
