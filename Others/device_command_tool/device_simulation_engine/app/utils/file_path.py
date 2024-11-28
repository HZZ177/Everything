#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午7:21
# @Author  : Heshouyi
# @File    : file_path.py
# @Software: PyCharm
# @description:

import os

'''项目目录'''
# 项目根目录，指向device_simulation_engine
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''一级目录'''
app_path = os.path.abspath(os.path.join(project_path, 'app'))       # app根目录
dev_config_path = os.path.abspath(os.path.join(project_path, 'config_dev.yml'))     # 开发环境配置文件
pro_config_path = os.path.abspath(os.path.join(project_path, 'config_pro.yml'))     # 正式环境配置文件
sqlite_path = os.path.abspath(os.path.join(project_path, 'SQlite'))     # SQlite数据库目录

'''二级目录'''
api_path = os.path.abspath(os.path.join(app_path, 'api'))
log_path = os.path.abspath(os.path.join(app_path, 'logs'))
models_path = os.path.abspath(os.path.join(app_path, 'models'))
utils_path = os.path.abspath(os.path.join(app_path, 'utils'))
connection_path = os.path.abspath(os.path.join(app_path, 'connection'))
resource_path = os.path.abspath(os.path.join(app_path, 'resource'))
db_path = os.path.abspath(os.path.join(sqlite_path, 'findcar_automation.db'))


if __name__ == '__main__':
    # print(resource_path)
    pass
