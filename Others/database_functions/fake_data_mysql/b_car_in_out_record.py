#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 11:18
# @Author  : Heshouyi
# @File    : b_car_in_out_record.py
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
        INSERT INTO b_car_in_out_record (
            lot_id, area_id, area_name, floor_id, floor_name, 
            element_park_id, park_addr, park_status, park_control, park_no, 
            plate_no, plate_no_simple, car_image_url, plate_no_color, 
            plate_no_record, in_time, out_time, in_type, out_type, 
            unique_id, create_time, creator, updater
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s
        )
        """

        data = []
        for _ in range(1000):
            lot_id = random.randint(1, 100)
            area_id = random.randint(1, 50)
            area_name = fake.word()
            floor_id = random.randint(1, 10)
            floor_name = fake.word()
            element_park_id = random.randint(1, 1000)
            park_addr = random.randint(1, 500)
            park_status = random.randint(0, 3)
            park_control = random.randint(0, 1)
            park_no = fake.word()
            plate_no = fake.license_plate()
            plate_no_simple = ''.join(filter(str.isalnum, plate_no))
            car_image_url = fake.image_url()
            plate_no_color = random.choice(['blue', 'yellow', 'white', 'green'])
            plate_no_record = ','.join([fake.license_plate() for _ in range(5)])
            in_time = fake.date_time_between(start_date='-1y', end_date='now')
            out_time = in_time + timedelta(hours=random.randint(1, 10))
            in_type = random.randint(0, 1)
            out_type = random.randint(0, 1)
            unique_id = str(uuid.uuid4()).replace("-", "")
            create_time = datetime.now()
            creator = fake.name()
            updater = fake.name()

            data.append((
                lot_id, area_id, area_name, floor_id, floor_name,
                element_park_id, park_addr, park_status, park_control, park_no,
                plate_no, plate_no_simple, car_image_url, plate_no_color,
                plate_no_record, in_time, out_time, in_type, out_type,
                unique_id, create_time, creator, updater
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
