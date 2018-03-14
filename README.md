## Introduction ##

Rest-Utils 为使用 SQLAlchemy (or Flask-SQLAlchemy) 定义的数据库模型提供简单的Restful APIs生成。
生成的API以JSON格式发送和接收消息。
使用 marshmallow 使得转换非常便捷。

For more information, see the

  * [documentation](https://windprog.github.io/rest-utils/),
  * [Python Package Index listing](https://pypi.python.org/pypi/rest-utils),
  * [source code repository](https://github.com/windprog/rest-utils).

# 实践教程介绍

该项目的目标是尽可能全面、简洁地说明Rest-Utils的功能

# 模型说明

    使用的模型为博客模型
    该模型提供了：用户关注、用户组、文章

## 部署说明：

    使用sqlite作为例子。
    
### 环境安装

* 下载
    * git clone https://github.com/windprog/rest-utils-sample
    * cd rest-utils-sample
* 安装依赖和重建数据库
    * bash init.sh

### 开发环境

    python run.py
    
### 自定义

* 创建数据库
    * create database sample_blog DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
* 更改mysql配置
    * 编辑：app.py 的 MYSQL_URI

# 本例模型阅读指引

## 多对多关系

    自引用："用户关注" --> User.followed
    用户组--用户 --> User.groups

## 一对多关系

    用户--文章 --> User.posts
    
## 一对一关系

    用户--注册校验  --> User.validation
    
## 约束相关
### 组合索引

    Group.__table_args__[1]

### 唯一约束

    Group.__table_args__[0]
