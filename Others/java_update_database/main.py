#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/17 14:46
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

    def get_all_tables_and_columns_from_database(self):

        self.connect_to_database()

        # 文件路径
        output_file = 'wanted_database_structure.txt'

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

    @staticmethod
    def load_structure_from_file(file_path):
        structure = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                current_table = None
                for line in file:
                    line = line.strip()
                    if line.startswith("Table:"):
                        current_table = line.split("Table: ")[1]
                        structure[current_table] = []
                    elif line.startswith("Field:") and current_table:
                        field_info = line.split(", ")
                        field_info_dict = {}
                        for info in field_info:
                            if ": " in info:
                                key, value = info.split(": ", 1)
                                field_info_dict[key.strip()] = value.strip() if value.strip() != 'None' else None
                        structure[current_table].append(field_info_dict)
        except Exception as e:
            print(f"读取文件结构失败: {e}")
            traceback.print_exc()
        return structure

    def get_current_database_structure(self):
        structure = {}
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"DESCRIBE `{table_name}`")
                    # 调试信息
                    # print(f"处理{table_name}")
                    columns = cursor.fetchall()
                    structure[table_name] = []
                    for column in columns:
                        field, type_ = column[:2]
                        structure[table_name].append({
                            "Field": field,
                            "Type": type_
                        })
        except Exception as e:
            print(f"获取当前数据库结构失败: {e}")
            traceback.print_exc()

        return structure

    @staticmethod
    def compare_structures(file_structure, db_structure):
        discrepancies = []

        for table in file_structure:
            if table not in db_structure:
                discrepancies.append(f"表 {table} 在数据库中不存在")
            else:
                file_columns = {col["Field"]: col for col in file_structure[table]}
                db_columns = {col["Field"]: col for col in db_structure[table]}

                for field in file_columns:
                    if field not in db_columns:
                        discrepancies.append(f"表 {table} 中的字段 {field} 在数据库中不存在")
                    else:
                        file_type = file_columns[field]["Type"]
                        db_type = db_columns[field]["Type"]
                        if file_type != db_type:
                            discrepancies.append(
                                f"表 {table} 中的字段 {field} 类型不一致: 文件中为 {file_type}, 数据库中为 {db_type}"
                            )

        for table in db_structure:
            if table not in file_structure:
                discrepancies.append(f"数据库中的表 {table} 在文件中不存在")

        return discrepancies

    def check_database_consistency(self, file_path):
        self.connect_to_database()
        file_structure = self.load_structure_from_file(file_path)
        current_db_structure = self.get_current_database_structure()
        discrepancies = self.compare_structures(file_structure, current_db_structure)

        if discrepancies:
            print("发现以下不一致：")
            for discrepancy in discrepancies:
                print(discrepancy)
        else:
            print("数据库结构与文件一致")

    def check_table_if_exist(self):
        # 预期的表名列表
        expected_tables = []

        try:
            with self.connection.cursor() as cursor:
                # 查询数据库中所有表名
                cursor.execute("SHOW TABLES")
                tables_in_db = cursor.fetchall()

                # 将结果转换为简单的列表
                tables_in_db = [table[0] for table in tables_in_db]
                print(tables_in_db)

                # 检查每个预期的表是否存在
                for table in expected_tables:
                    if table in tables_in_db:
                        print(f"表 '{table}' 存在于数据库中。")
                    else:
                        print(f"表 '{table}' 不存在于数据库中。")
        finally:
            self.connection.close()


if __name__ == "__main__":
    app = Application(host="localhost", port=5831, user="root", password="Keytop:wabjtam!", database='ktpark')

    # 获取标准库结构
    # app.get_all_tables_and_columns_from_database()

    # 检查数据库结构是否一致
    app.check_database_consistency('wanted_database_structure.txt')
