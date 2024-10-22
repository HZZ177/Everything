#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/11 14:09
# @Author  : Heshouyi
# @File    : api_supplementary_push.py
# @Software: PyCharm
# @description:
import pymysql
from faker import Faker
import random
import uuid
from tqdm import tqdm
import time
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed


class DataGenerator:
    def __init__(self, db_config):
        self.fake = Faker()
        self.db_config = db_config

    def generate_data(self, batch_size):
        """
        生成用于插入数据库的数据集
        :param batch_size:
        :return: 数据列表
        """
        data = []
        for _ in range(batch_size):
            url = self.fake.url()
            header = self.fake.text(max_nb_chars=50)
            params = self.fake.text(max_nb_chars=50)
            reason = self.fake.text(max_nb_chars=50)
            status = random.randint(0, 1)
            req_id = str(uuid.uuid4()).replace('-', '')
            create_time = self.fake.date_time_between(start_date='-2y', end_date='now')

            data.append((url, header, params, reason, status, req_id, create_time))

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
        执行数据生成和插入的过程
        :param num_records: 总数据量
        :param batch_size: 每次批量插入的大小
        :param num_threads: 并行生成数据的线程数
        """
        sql = """
        INSERT INTO api_supplementary_push (
            url, header, params, reason, status, req_id, create_time
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
        """

        start_time = time.time()

        # 1. 数据生成阶段
        gen_start_time = time.time()
        all_data = []

        with tqdm(total=num_records // batch_size, desc="数据生成进度") as pbar:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [
                    executor.submit(self.generate_data, batch_size)
                    for _ in range(num_records // batch_size)
                ]

                for future in as_completed(futures):
                    data = future.result()
                    all_data.extend(data)
                    pbar.update(1)

        gen_end_time = time.time()

        # 2. 数据插入阶段
        insert_start_time = time.time()
        with tqdm(total=len(all_data) // batch_size, desc="数据插入进度") as pbar:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for i in range(0, len(all_data), batch_size):
                    batch_data = all_data[i:i + batch_size]
                    futures.append(executor.submit(self.insert_data, sql, batch_data))

                for future in as_completed(futures):
                    pbar.update(1)

        insert_end_time = time.time()

        end_time = time.time()

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

    num_records = 10000    # 生成数据总量
    batch_size = 1000      # 每批次数据大小
    num_threads = 4        # 生成数据并行线程数

    generator = DataGenerator(db_config)
    generator.run(num_records, batch_size, num_threads)
