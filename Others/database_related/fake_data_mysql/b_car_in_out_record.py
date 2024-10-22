#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 13:43
# @Author  : Heshouyi
# @File    : optimized_data_generator.py
# @Software: PyCharm
# @description:

import yaml
from faker import Faker
import pymysql
import uuid
from datetime import timedelta
import random
import string
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


class DataGenerator:
    def __init__(self, db_config):
        self.fake = Faker()
        self.db_config = db_config

    @staticmethod
    def generate_chinese_license_plate():
        """
        生成符合格式的中国车牌
        :return:
        """
        province = random.choice([
            '京', '津', '沪', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁',
            '新', '苏', '浙', '赣', '鄂', '桂', '甘', '晋', '蒙', '陕', '吉', '闽',
            '贵', '粤', '青', '藏', '川', '宁', '琼'
        ])
        letter = random.choice(string.ascii_uppercase)
        numbers = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"{province}{letter}{numbers}"

    def generate_data(self, batch_size):
        """
        预先生成用于插入数据库的数据集
        :param batch_size:
        :return:
        """
        data = []
        for _ in range(batch_size):
            lot_id = 1
            area_id = random.randint(1, 50)
            area_name = self.fake.word()
            floor_id = random.randint(1, 10)
            floor_name = self.fake.word()
            element_park_id = random.randint(1, 1000)
            park_addr = random.randint(100000, 500000)
            park_status = random.randint(0, 3)
            park_control = random.randint(0, 1)
            park_no = self.fake.word()
            plate_no = self.generate_chinese_license_plate()
            plate_no_simple = plate_no[1:]
            car_image_url = self.fake.image_url()
            plate_no_color = random.choice(['蓝', '黄', '白', '绿'])
            plate_no_record = ','.join([self.generate_chinese_license_plate() for _ in range(5)])
            in_time = self.fake.date_time_between(start_date='-2y', end_date='now')
            out_time = in_time + timedelta(hours=random.randint(1, 10))
            in_type = random.randint(0, 1)
            out_type = random.randint(0, 1)
            unique_id = str(uuid.uuid4()).replace("-", "")
            create_time = self.fake.date_time_between(start_date='-2y', end_date='now')
            creator = 'data_creator'
            updater = 'data_creator'

            data.append((
                lot_id, area_id, area_name, floor_id, floor_name,
                element_park_id, park_addr, park_status, park_control, park_no,
                plate_no, plate_no_simple, car_image_url, plate_no_color,
                plate_no_record, in_time, out_time, in_type, out_type,
                unique_id, create_time, creator, updater
            ))

        return data

    def insert_data(self, sql, data_batch):
        """
        将数据批量插入数据库
        :param sql: SQL 插入语句
        :param data_batch: 一批待插入的数据
        """
        connection = pymysql.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['dbname']
        )
        try:
            with connection.cursor() as cursor:
                cursor.executemany(sql, data_batch)
                connection.commit()
        finally:
            connection.close()

    def run(self, num_records, batch_size, num_threads):
        """
        运行生成数据和插入数据库的过程
        :return:
        """
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

        start_time = time.time()  # 程序开始时间

        # 1. 生成数据阶段
        gen_start_time = time.time()  # 数据生成开始时间
        all_data = []  # 存放生成的所有数据

        # 提前显示进度条
        with tqdm(total=num_records // batch_size, desc="数据生成进度") as pbar:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(self.generate_data, batch_size) for _ in range(num_records // batch_size)]

                for future in as_completed(futures):
                    data = future.result()  # 获取生成的数据
                    all_data.extend(data)  # 收集所有数据
                    pbar.update(1)  # 每完成一个线程，进度条更新

        gen_end_time = time.time()  # 数据生成结束时间

        # 2. 插入数据阶段
        insert_start_time = time.time()  # 插入数据库开始时间
        with tqdm(total=len(all_data) // batch_size, desc="数据插入进度") as pbar:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for i in range(0, len(all_data), batch_size):
                    batch_data = all_data[i:i + batch_size]
                    futures.append(executor.submit(self.insert_data, sql, batch_data))

                for future in as_completed(futures):
                    pbar.update(1)

        insert_end_time = time.time()  # 插入数据库结束时间

        end_time = time.time()  # 程序结束时间

        print(f"数据生成总时间: {gen_end_time - gen_start_time: .2f}秒")
        print(f"数据库插入总时间: {insert_end_time - insert_start_time: .2f}秒")
        print(f"程序总时间: {end_time - start_time: .2f}秒")


def load_db_config():
    """
    从dbconfig.yml加载数据库配置信息
    :return: 数据库配置字典
    """
    with open("dbconfig.yml", "r") as file:
        config = yaml.safe_load(file)
    return config['database']


if __name__ == '__main__':
    # 从配置文件中加载数据库信息
    db_config = load_db_config()

    num_records = 5000000  # 生成数据总量
    batch_size = 10000  # 每批次数据大小，分批执行提升效率
    num_threads = 8  # 生成数据并行线程数

    generator = DataGenerator(db_config)
    generator.run(num_records, batch_size, num_threads)
