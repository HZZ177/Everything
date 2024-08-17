#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/10 下午2:07
# @Author  : Heshouyi
# @File    : db_tool.py
# @Software: PyCharm
# @description: 封装各个数据库操作工具

import pymysql
from findcar_auto.common.log_tool import logger
from findcar_auto.common.config_loader import configger


config = configger.load_config()


class DBTool:
    def __init__(self):
        self.connection = pymysql.connect(
            host=config.get('db').get('host'),
            user=config.get('db').get('user'),
            password=config.get('db').get('password'),
            db=config.get('db').get('database'),
            port=config.get('db').get('port'),
        )

    def query(self, sql, params=None):
        """
        查询数据库数据
        :param sql: SQL查询语句
        :param params: 参数列表，用于参数化查询
        :return: 查询结果
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f'查询数据库SQL语句{sql}失败，错误信息：{e}')
            raise   # 抛出异常以便上层业务处理

    def execute(self, sql, params=None):
        """
        执行sql语句
        :param sql: SQL语句
        :param params: 参数列表用于参数化查询
        :return: bool
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
                return True
        except Exception as e:
            logger.error(f'执行数据库SQL语句{sql}失败，错误信息：{e}')
            # 如果报错，回滚提交的事务
            self.connection.rollback()
            raise   # 抛出异常以便上层业务处理

    def close(self):
        self.connection.close()






