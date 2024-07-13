#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/13 下午11:47
# @Author  : Heshouyi
# @File    : delete_database_structure.py
# @Software: PyCharm
# @description:

import pymysql


def delete_database_structure():
    # 连接数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Keytop:wabjtam!',
        database='parking_guidance',
        port=5831
    )
    cursor = connection.cursor()

    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 修改每个表
    for table in tables:
        table_name = table[0]

        # 获取所有字段信息
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()

        # 删除除id之外的所有字段
        for column in columns:
            column_name = column[0]
            if column_name != 'id':
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")

        # 获取所有索引信息
        cursor.execute(f"SHOW INDEX FROM {table_name}")
        indexes = cursor.fetchall()

        # 删除所有索引
        for index in indexes:
            index_name = index[2]  # 索引名在第三列
            if index_name != 'PRIMARY':  # 保留主键索引
                cursor.execute(f"ALTER TABLE {table_name} DROP INDEX {index_name}")
        print(f'表{table_name}除主键id外所有字段和索引清除完成')
    connection.commit()

    # 关闭连接
    cursor.close()
    connection.close()


if __name__ == '__main__':
    delete_database_structure()
