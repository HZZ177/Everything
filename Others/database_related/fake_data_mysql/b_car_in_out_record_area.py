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
import string
from tqdm import tqdm
import time

fake = Faker()


def generate_chinese_license_plate():
    province = random.choice([
        '京', '津', '沪', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁',
        '新', '苏', '浙', '赣', '鄂', '桂', '甘', '晋', '蒙', '陕', '吉', '闽',
        '贵', '粤', '青', '藏', '川', '宁', '琼'
    ])
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{province}{letter}{numbers}"


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
        num_records = 1000000
        batch_size = 1000

        # 开始计时
        start_time = time.time()
        data_gen_time = 0
        db_insert_time = 0

        for _ in tqdm(range(num_records), desc="Inserting records"):

            # 记录数据生成时间
            gen_start_time = time.time()

            area_camera_id = random.randint(1, 10)
            area_camera_ip = fake.ipv4()
            event_id = str(uuid.uuid4()).replace('-', '')
            floor_id = random.randint(1, 10)
            floor_name = fake.word()
            area_id = random.randint(1, 50)
            area_name = fake.word()
            plate_no = generate_chinese_license_plate()
            plate_no_simple = plate_no[1:]
            plate_no_color = random.choice(['blue', 'yellow', 'white', 'green'])
            car_image_url = fake.image_url()
            event_type = random.randint(1, 2)
            in_out_time = fake.date_time_between(start_date='-2y', end_date='now')
            create_time = fake.date_time_between(start_date='-2y', end_date='now')
            creator = fake.name()
            updater = fake.name()

            data.append((
                area_camera_id, area_camera_ip, event_id, floor_id, floor_name,
                area_id, area_name, plate_no, plate_no_simple, plate_no_color,
                car_image_url, event_type, in_out_time, create_time, creator, updater
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