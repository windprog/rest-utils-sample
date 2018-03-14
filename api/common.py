#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author  :   windpro
E-mail  :   windprog@gmail.com
Date    :   2018/3/14
Desc    :   
"""
def add_project_path():
    import os
    import sys

    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(PROJECT_PATH)
    if PROJECT_PATH not in sys.path:
        sys.path.append(PROJECT_PATH)

add_project_path()
