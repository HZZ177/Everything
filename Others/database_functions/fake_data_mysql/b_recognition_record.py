#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:43
# @Author  : Heshouyi
# @File    : b_recognition_record.py
# @Software: PyCharm
# @description:
from faker import Faker
import pymysql
from datetime import datetime
import random
import string


fake = Faker("zh_CN")


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
        INSERT INTO b_recognition_record (
            park_addr, plate_no, plate_no_simple, car_image_url, plate_no_reliability, create_time
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
        """

        data = []
        for _ in range(1000):
            park_addr = random.randint(1, 500)
            plate_no = generate_chinese_license_plate()
            plate_no_simple = plate_no[1:]
            car_image_url = fake.image_url()
            plate_no_reliability = random.randint(0, 100)
            create_time = datetime.now()

            data.append((
                park_addr, plate_no, plate_no_simple, car_image_url, plate_no_reliability, create_time
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

