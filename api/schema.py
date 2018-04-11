#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/3/14
Desc    :   
"""
import common
import random
from rest_utils import ModelSchema
from rest_utils import fields
from models import Group, User


class GroupSchema(ModelSchema):
    """
    marshmallow使用例子，更详细使用可参见：http://marshmallow.readthedocs.io/
    实现自定义字段
    """
    sort = fields.Method(
        serialize='get_sort',
        deserialize='load_sort'
    )

    def get_sort(self, obj):
        return random.randint(0, 10)

    def load_sort(self, value):
        print "loading sort", value

    class Meta:
        model = Group


class UserSchema(ModelSchema):
    """
    实现User.groups下字段自定义
    """

    class UserGroupSchema(ModelSchema):
        user_sort = fields.Function(lambda obj: random.randint(10, 20))

        class Meta:
            model = Group

    groups = fields.Related(UserGroupSchema)

    class Meta:
        model = User
