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
from tqdm import tqdm
import time

fake = Faker()

# 连接数据库
connection = pymysql.connect(
    host='192.168.21.249',
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
        num_records = 1000000
        batch_size = 1000

        # 开始计时
        start_time = time.time()
        data_gen_time = 0
        db_insert_time = 0

        for _ in tqdm(range(num_records), desc="Inserting records"):

            # 记录数据生成时间
            gen_start_time = time.time()

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

            gen_end_time = time.time()
            data_gen_time += (gen_end_time - gen_start_time)
            # 每1000条数据批量插入一次
            if len(data) == batch_size:
                insert_start_time = time.time()

                cursor.executemany(sql, data)
                connection.commit()

                insert_end_time = time.time()
                db_insert_time += (insert_end_time - insert_start_time)

                data = []

        # 插入剩余数据
        if data:
            cursor.executemany(sql, data)
            connection.commit()

            insert_end_time = time.time()
            db_insert_time += (insert_end_time - insert_start_time)

        end_time = time.time()

        print(f"数据生成时间: {data_gen_time: .2f}秒")
        print(f"数据库插入时间: {db_insert_time: .2f}秒")
        print(f"总时间: {end_time - start_time: .2f}秒")


finally:
    connection.close()
