#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 14:09
# @Author  : Heshouyi
# @File    : api_supplementary_push.py
# @Software: PyCharm
# @description:
import pymysql
from faker import Faker
from datetime import datetime
import random
import uuid

fake = Faker()

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    port=5831,
    user='root',
    password='Keytop:wabjtam!',
    database='parking_guidance'
)

try:
    with connection.cursor() as cursor:
        # 插入数据
        sql = """
        INSERT INTO api_supplementary_push (
            url, header, params, reason, status, req_id, create_time
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
        """

        data = []
        for _ in range(1000):
            url = fake.url()
            header = fake.text(max_nb_chars=50)
            params = fake.text(max_nb_chars=50)
            reason = fake.text(max_nb_chars=50)
            status = random.randint(0, 1)
            req_id = str(uuid.uuid4()).replace('-', '')
            create_time = fake.date_time_between(start_date='-2y', end_date='now')

            data.append((
                url, header, params, reason, status, req_id, create_time
            ))

            # 每1000条数据批量插入一次
            if len(data) == 1000:
                cursor.executemany(sql, data)
                connection.commit()
                data = []

        # 插入剩余数据
        if data:
            cursor.executemany(sql, data)
            connection.commit()

finally:
    connection.close()
