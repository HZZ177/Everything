#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/19 17:11
# @Author  : Heshouyi
# @File    : main_parking_guidance.py
# @Software: PyCharm
# @description:
import pymysql
import traceback
from time import sleep


class Application:

    def __init__(self, host, port, user, password, database):
        """
        针对目前版本的寻车标准数据库生成对应的所有创建表语句、插入字段语句、插入索引语句
        :param host: 数据库IP
        :param port: 数据库端口
        :param user: 连接用户名
        :param password: 连接密码
        :param database: 指定数据库名称
        """
        # 数据库连接参数
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        # 文件路径
        self.output_file = 'output/ktpark_database_structure_fix.sql'

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
        """
        获取标准库结构，只包含表名，字段和字段类型
        :return:
        """

        self.connect_to_database()

        # 文件路径
        output_file = 'output/ktpark_database_structure.txt'

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

    def insert_procedure_sentences(self):
        procedure_add_element_unless_exists = """
DROP PROCEDURE IF EXISTS add_element_unless_exists;
DELIMITER $$
-- 新增字段或索引，新增之前会判定是否存在
-- element_type：参数类型 column=字段 index=索引
-- tab_name：表名
-- element_name：字段名或索引名
-- sql_statement：执行的sql
CREATE PROCEDURE add_element_unless_exists(IN element_type VARCHAR(64), IN tab_name VARCHAR(64), IN element_name VARCHAR(64), IN sql_statement VARCHAR(500))
BEGIN

    -- 新增字段
    IF element_type = 'column' THEN
        IF NOT EXISTS (
            -- 判定字段是否存在
            SELECT * FROM information_schema.columns
            WHERE table_schema = DATABASE() and table_name = tab_name AND column_name = element_name
        ) THEN
            SET @s = sql_statement;
            PREPARE stmt FROM @s;
            EXECUTE stmt;
        END IF;
    END IF;

    -- 新增索引
    IF element_type = 'index' THEN
        IF NOT EXISTS (
            -- 判定索引是否存在
            SELECT 1 FROM INFORMATION_SCHEMA.STATISTICS
            WHERE table_schema = DATABASE() and table_name= tab_name AND index_name= element_name
        ) THEN
            SET @s = sql_statement;
            PREPARE stmt FROM @s;
            EXECUTE stmt;
        END IF;
    END IF;

END; $$
DELIMITER ;
"""

        with open(self.output_file, 'w', encoding="utf-8") as file:
            file.write(f"-- ============定义存储过程============\n")
            file.write(f"{procedure_add_element_unless_exists}\n\n")

    def get_all_construct_sentences(self):
        """
        获取所有表创建语句
        :return:
        """

        self.connect_to_database()

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量创建标准库表===============\n")
                    for table in tables:
                        table_name = table[0]
                        file.write(f"-- 构造表 {table_name}\n")

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
        """
        获取所有字段和索引创建语句
        :return:
        """

        self.connect_to_database()

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量更新所有表字段===============\n")
                    for table in tables:
                        table_name = table[0]
                        # file.write(f"-- 构造表{table_name}\n")

                        # 调试输出
                        # print(f"正在处理表: {table_name}")

                        # 获取所有表的初始化语句
                        cursor.execute(f"""SELECT
                                                COLUMN_NAME,
                                                DATA_TYPE,
                                                IS_NULLABLE,
                                                COLUMN_DEFAULT,
                                                CHARACTER_MAXIMUM_LENGTH,
                                                NUMERIC_PRECISION,
                                                COLUMN_TYPE,
                                                COLUMN_KEY,
                                                EXTRA 
                                            FROM
                                                INFORMATION_SCHEMA.COLUMNS 
                                            WHERE
                                                TABLE_SCHEMA = '{self.database}' 
                                                AND TABLE_NAME = '{table_name}';
                                                """)
                        create_columns = cursor.fetchall()
                        fields = str(create_columns).split(r'\n')

        except Exception as e:
            print(f"获取{table_name}表结构信息失败: {e}")
            traceback.print_exc()

        sleep(2)


if __name__ == "__main__":
    app = Application(host="localhost", port=5831, user="root", password="Keytop:wabjtam!", database='ktpark')

    # 获取标准库结构
    # app.get_all_tables_and_columns()

    # 写入存储过程
    app.insert_procedure_sentences()

    # 获取所有表创建语句
    app.get_all_construct_sentences()

    # 获取所有字段和索引创建语句
    app.get_all_column_insert_sentences()
