#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/14 15:04
# @Author  : Heshouyi
# @File    : drop_tables.py
# @Software: PyCharm
# @description:
import pymysql

# 连接数据库
connection = pymysql.connect(
    host='192.168.21.249',
    port=5831,
    user='root',
    password='Keytop:wabjtam!',
    database='parking_guidance'
)


try:
    # b_car_in_out_record清理
    with connection.cursor() as cursor:
        # 查询所有以 b_car_in_out_record_202 开头的表名
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'parking_guidance' 
              AND table_name LIKE 'b_car_in_out_record_202%'
        """)
        tables_record = cursor.fetchall()

        # 生成并执行 DROP TABLE 语句
        for table in tables_record:
            drop_table_sql = f"DROP TABLE {table[0]}"
            cursor.execute(drop_table_sql)
    # 提交更改
    connection.commit()

    # b_car_in_out_record_area清理
    with connection.cursor() as cursor:
        # 查询所有以 b_car_in_out_record_area_202 开头的表名
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'parking_guidance' 
              AND table_name LIKE 'b_car_in_out_record_area_202%'
        """)
        tables_record_area = cursor.fetchall()

        # 生成并执行 DROP TABLE 语句
        for table in tables_record_area:
            drop_table_sql = f"DROP TABLE {table[0]}"
            cursor.execute(drop_table_sql)
    # 提交更改
    connection.commit()

    # api_supplementary_push清理
    with connection.cursor() as cursor:
        # 查询所有以 api_supplementary_push_202 开头的表名
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'parking_guidance' 
              AND table_name LIKE 'api_supplementary_push_202%'
        """)
        tables_supplementary_push = cursor.fetchall()

        # 生成并执行 DROP TABLE 语句
        for table in tables_supplementary_push:
            drop_table_sql = f"DROP TABLE {table[0]}"
            cursor.execute(drop_table_sql)
    # 提交更改
    connection.commit()

    # b_recognition_record清理
    with connection.cursor() as cursor:
        # 查询所有以 b_recognition_record_202 开头的表名
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'parking_guidance' 
              AND table_name LIKE 'b_recognition_record_202%'
        """)
        tables_supplementary_push = cursor.fetchall()

        # 生成并执行 DROP TABLE 语句
        for table in tables_supplementary_push:
            drop_table_sql = f"DROP TABLE {table[0]}"
            cursor.execute(drop_table_sql)
    # 提交更改
    connection.commit()

finally:
    connection.close()
