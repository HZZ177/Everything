#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/19 17:11
# @Author  : Heshouyi
# @File    : main.py
# @Software: PyCharm
# @description:
import pymysql
import traceback
from time import sleep


class Application:

    def __init__(self, host, port, user, password, database):
        # 数据库连接参数
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect_to_database(self):
        try:
            # 连接到数据库
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                connect_timeout=10,  # 连接超时时间，单位秒
                read_timeout=10  # 读取超时时间，单位秒
            )
        except Exception as e:
            print(f"数据库连接失败: {e}")
            traceback.print_exc()

    def get_all_tables_and_columns(self):

        self.connect_to_database()

        # 文件路径
        output_file = 'database_structure.txt'

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(output_file, 'w', encoding="utf-8") as file:
                    for table in tables:
                        table_name = table[0]
                        file.write(f"Table: {table_name}\n")

                        # 调试输出
                        # print(f"正在处理表: {table_name}")

                        # 获取表中的所有字段名和字段类型
                        cursor.execute(f"DESCRIBE `{table_name}`")
                        columns = cursor.fetchall()

                        for column in columns:
                            field, type_ = column[:2]
                            file.write(f"  Field: {field}, Type: {type_}\n")

                        file.write("\n")

        except Exception as e:
            print(f"获取表和列信息失败: {e}")
            traceback.print_exc()

        sleep(2)

    def get_all_construct_sentences(self):

        self.connect_to_database()

        # 文件路径
        output_file = 'database_construct_sentences.sql'

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(output_file, 'w', encoding="utf-8") as file:
                    for table in tables:
                        table_name = table[0]
                        file.write(f"-- 构造表{table_name}\n")

                        # 调试输出
                        # print(f"正在处理表: {table_name}")

                        # 获取所有表的初始化语句
                        cursor.execute(f"show create TABLE `{table_name}`")
                        columns = cursor.fetchall()

                        for column in columns:
                            describe = column[1]
                            file.write(f"CREATE TABLE IF NOT EXISTS{str(describe).replace("CREATE TABLE", "")};\n")

                        file.write("\n")

        except Exception as e:
            print(f"获取表结构信息失败: {e}")
            traceback.print_exc()

        sleep(2)

    def get_all_column_insert_sentences(self):

        self.connect_to_database()

        # 文件路径
        output_file = 'column_insert_sentences.sql'

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(output_file, 'w', encoding="utf-8") as file:
                    for table in tables:
                        table_name = table[0]
                        # file.write(f"-- 构造表{table_name}\n")

                        # 调试输出
                        # print(f"正在处理表: {table_name}")

                        # 获取所有表的初始化语句
                        cursor.execute(f"show create TABLE `{table_name}`")
                        create_sentences = cursor.fetchall()
                        fields = str(create_sentences).split(r'\n')

                        # 获取所有字段的字符串并初步规范格式
                        sentences = str(fields[2:][:-1]).replace("  ", "").replace(',"', '"').split(", ")
                        file.write(f"-- 表{table_name}字段创建语句\n")
                        for sentence in sentences:
                            column_id = 0

                            # 控制添加索引的字段的格式，去除前后引号
                            if sentence[0] != "`":
                                sentence.replace("'", "")
                            # 规范所有单句的格式
                            format_sentence = sentence.replace("[", "").replace("]", "").replace(",", "").replace('"', "").replace("'", '"')

                            # 开始生成调取存储过程的字段生成语句
                            if format_sentence[0] == "`":
                                column = format_sentence.split("`")[1]
                                if column_id < 1:
                                    file.write(f"CALL add_element_unless_exists('column', '{table_name}', '{column}', 'ALTER TABLE {table_name} ADD COLUMN {format_sentence}');\n")
                                file.write(f"CALL add_element_unless_exists('column', '{table_name}', '{column}', 'ALTER TABLE {table_name} ADD COLUMN {format_sentence}');\n")

                        file.write("\n")

        except Exception as e:
            print(f"获取表结构信息失败: {e}")
            traceback.print_exc()

        sleep(2)


if __name__ == "__main__":
    app = Application(host="localhost", port=5831, user="root", password="Keytop:wabjtam!", database='parking_guidance')

    # 获取标准库结构
    # app.get_all_tables_and_columns()

    # 获取所有表创建语句
    # app.get_all_construct_sentences()

    # 获取所有字段创建语句
    app.get_all_column_insert_sentences()
