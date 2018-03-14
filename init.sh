#! /bin/sh
# Author: Windpro Zhao <windprog@gmail.com>

# 安装依赖
pip install -r requirements.txt
# 同步表结构
# alembic upgrade head
cd api
python app.py
