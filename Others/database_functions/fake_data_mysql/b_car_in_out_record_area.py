#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 11:40
# @Author  : Heshouyi
# @File    : b_car_in_out_record_area.py
# @Software: PyCharm
# @description:
from faker import Faker
import pymysql
import uuid
from datetime import datetime, timedelta
import random

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
        INSERT INTO b_car_in_out_record_area (
            area_camera_id, area_camera_ip, event_id, floor_id, floor_name,
            area_id, area_name, plate_no, plate_no_simple, plate_no_color,
            car_image_url, type, in_out_time, create_time, creator, updater
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        """

        data = []
        for _ in range(1000):
            area_camera_id = random.randint(1, 500)
            area_camera_ip = fake.ipv4()
            event_id = str(uuid.uuid4()).replace('-', '')
            floor_id = random.randint(1, 10)
            floor_name = fake.word()
            area_id = random.randint(1, 50)
            area_name = fake.word()
            plate_no = fake.license_plate()
            plate_no_simple = ''.join(filter(str.isalnum, plate_no))
            plate_no_color = random.choice(['blue', 'yellow', 'white', 'green'])
            car_image_url = fake.image_url()
            event_type = random.randint(1, 2)
            in_out_time = fake.date_time_between(start_date='-1y', end_date='now')
            create_time = datetime.now()
            creator = fake.name()
            updater = fake.name()

            data.append((
                area_camera_id, area_camera_ip, event_id, floor_id, floor_name,
                area_id, area_name, plate_no, plate_no_simple, plate_no_color,
                car_image_url, event_type, in_out_time, create_time, creator, updater
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
