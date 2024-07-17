#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/19 17:11
# @Author  : Heshouyi
# @File    : main_parking_guidance.py
# @Software: PyCharm
# @description:
import os
import re
import shutil

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
        self.output_data_path = 'output'
        self.output_file_path = os.path.join(self.output_data_path, 'parking_guidance_database_structure_fix.sql')

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
        output_file = 'output/parking_guidance_database_structure.txt'

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
    -- 设置字符集为 utf8mb4
    SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
    SET CHARACTER SET utf8mb4;
    
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
        # 确保输出路径存在
        if not os.path.exists(self.output_data_path):
            os.makedirs(self.output_data_path)

        with open(self.output_file_path, 'w', encoding="utf-8") as file:
            file.write("SET NAMES utf8mb4;\n")
            file.write("SET CHARACTER SET utf8mb4;\n")
            # file.write("ALTER DATABASE parking_guidance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n\n")
            file.write("-- ============定义存储过程============\n")
            file.write(f"{procedure_add_element_unless_exists}\n\n")

    def get_all_construct_sentences(self):
        """
        获取所有表创建语句并动态生成目标语句
        :return:
        """

        self.connect_to_database()

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file_path, 'a', encoding="utf-8") as file:
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
        获取所有字段和索引动态生成结构修补语句
        :return:
        """

        self.connect_to_database()

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file_path, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量更新所有表字段===============\n")
                    for table in tables:
                        table_name = table[0]

                        # 获取所有表的初始化语句
                        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                        create_sentences = cursor.fetchall()
                        fields = str(create_sentences).split(r'\n')[1:][:-1]

                        # 获取所有的表级别注释
                        cursor.execute(f"SHOW TABLE STATUS LIKE '{table_name}'")
                        table_status = cursor.fetchone()
                        table_comment = table_status[17] if table_status else None

                        # 使用正则表达式单独分组COMMENT之前和之后的内容，方便分开处理格式规范
                        processed_fields = []
                        comments = []
                        for field in fields:
                            match = re.match(r"^(.*?)( COMMENT '.*')?,?$", field.strip())
                            if match:
                                base_definition = match.group(1)
                                comment_part = match.group(2) if match.group(2) else ""
                                processed_fields.append(base_definition)
                                comments.append(comment_part)

                        # 获取所有字段的字符串并初步规范格式
                        sentences = str(processed_fields
                                        ).replace(',"', '"').replace("'`", '"`'
                                        ).replace("NULL'", 'NULL"').replace("TIMESTAMP'", 'TIMESTAMP"'
                                        ).replace("longtext'", 'longtext"').split(", ")

                        # 开始生成结构修正语句
                        file.write(f"-- 更新表 {table_name} 所有字段和索引\n")
                        # file.write(f"ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\n")
                        file.write(f"ALTER TABLE {table_name} COMMENT = '{table_comment}';\n")
                        file.write(f"ALTER TABLE {table_name} ROW_FORMAT=DYNAMIC;\n")

                        # 初始化当前表中的字段位置计数器
                        column_id = 0
                        # 储存上一个字段用于编写 after xx
                        column_pre = None

                        for i, sentence in enumerate(sentences):
                            if len(sentence) < 20:
                                continue
                            # 控制添加索引的字段的格式，去除前后引号
                            if sentence[0] != "`":
                                sentence.replace("'", "")
                            # 规范所有主句部分的格式
                            processed_format_sentence = sentence.replace("[", "").replace("]", "").replace('"', "").replace("'", '"')

                            # 拼接COMMENT部分
                            final_sentence = processed_format_sentence + (comments[i].replace("'", '"') if comments[i] else '')

                            # 如果检测到当前语句是以字段开头，则开始生成调取存储过程的字段生成语句，否则则生成索引插入语句
                            if final_sentence[0] == "`" or final_sentence.startswith('"`'):
                                column_now = final_sentence.split("`")[1]
                                if column_id < 1:
                                    file.write(
                                        f"CALL add_element_unless_exists('column', '{table_name}', '{column_now}', 'ALTER TABLE {table_name} ADD COLUMN {final_sentence};');\n")
                                else:
                                    file.write(
                                        f"CALL add_element_unless_exists('column', '{table_name}', '{column_now}', 'ALTER TABLE {table_name} ADD COLUMN {final_sentence} AFTER {column_pre};');\n")
                                column_pre = column_now
                                column_id += 1
                            elif 'PRIMARY' not in final_sentence:
                                key_name = final_sentence.split("`")[1]
                                key = final_sentence.split("(`")[1].split("`")[0]
                                if "udx" in key_name:
                                    file.write(f"CALL add_element_unless_exists('index', '{table_name}', '{key_name}', 'ALTER TABLE {table_name} ADD UNIQUE INDEX {key_name} ({key}) USING BTREE');\n")
                                else:
                                    file.write(f"CALL add_element_unless_exists('index', '{table_name}', '{key_name}', 'ALTER TABLE {table_name} ADD INDEX {key_name} ({key}) USING BTREE');\n")
                        file.write("\n")

        except Exception as e:
            print(f"获取{table_name}表结构信息失败: {e}")
            traceback.print_exc()

        sleep(2)

    def force_copy_file_to(self, dest):
        """
        强制复制输出的structure_fix文件到另一个路径，作为依赖文件
        :param dest: 目标文件路径
        """
        src = self.output_file_path

        try:
            # 确保目标目录存在
            dest_dir = os.path.dirname(dest)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # 复制文件并覆盖目标路径中的同名文件
            shutil.copy2(src, dest)
            print(f"文件已复制到 {dest}")

        except Exception as e:
            print(f"复制文件失败: {e}")


if __name__ == "__main__":
    # 连接云端基线库，只读权限账号，获取3.2.3数据库标准结构
    app = Application(host="101.91.144.186", port=13049, user="keytop", password="Keytop@2024", database='parking_guidance_3.2.3')

    # 写入存储过程
    app.insert_procedure_sentences()
    # 获取所有表创建语句并动态生成目标语句
    app.get_all_construct_sentences()
    # 获取所有字段和索引动态生成结构修补语句
    app.get_all_column_insert_sentences()

    # 文件动态生成完成后强制同步到update_database_tool项目作为依赖文件
    destination_file = '../update_database_tool/data/parking_guidance_database_structure_fix.sql'
    app.force_copy_file_to(destination_file)
