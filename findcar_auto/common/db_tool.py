#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/10 下午2:07
# @Author  : Heshouyi
# @File    : db_tool.py
# @Software: PyCharm
# @description: 封装各个数据库操作工具

import pymysql


class DBTool:
    def __init__(self, host, user, password, db, port=3306):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
        )

    def query(self, sql, params=None):
        """
        查询数据库数据
        :param sql:
        :param params:
        :return: 查询结果
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def execute(self, sql, params=None):
        """
        执行sql语句
        :param sql:
        :param params:
        :return:
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()

    def close(self):
        self.connection.close()






