#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/13 下午6:13
# @Author  : Heshouyi
# @File    : parking_guidance_update_tool.py
# @Software: PyCharm
# @description:

import os
import subprocess
import pymysql
from delete_database_structure import delete_database_structure


class UpdateDatabase:

    def __init__(self, old_db_host, new_db_host, old_db_name="parking_guidance", new_db_name="parking_guidance_test"):
        self.old_database_host = old_db_host
        self.new_database_host = new_db_host
        self.old_database_name = old_db_name
        self.new_database_name = new_db_name

        # 旧数据库配置
        self.old_db_config = {
            'host': self.old_database_host,
            'port': 5831,
            'user': 'root',
            'password': 'Keytop:wabjtam!',
            'database': self.old_database_name
        }

        # 新数据库配置
        self.new_db_config = {
            'host': self.new_database_host,
            'port': 5831,
            'user': 'root',
            'password': 'Keytop:wabjtam!',
            'database': self.new_database_name,
            'charset': 'utf8mb4'
        }

        # mysqldump文件相关变量
        self.old_db_dump_file = 'data/old_db_backup_file.sql'
        self.old_db_fixed_dump_file = 'data/old_db_fixed_file.sql'
        self.new_db_backup_file = 'data/new_db_backup_file.sql'
        self.db_structure_fix_file = 'data/parking_guidance_database_structure_fix.sql'

    def connect_database(self, which):
        try:
            # 连接到数据库
            if 'old' in which:
                conn = pymysql.connect(
                    host=self.old_db_config['host'],
                    user=self.old_db_config['user'],
                    password=self.old_db_config['password'],
                    port=self.old_db_config['port'],
                    database=self.old_db_config['database']  # 确保连接到正确的数据库
                )
            else:
                conn = pymysql.connect(
                    host=self.new_db_config['host'],
                    user=self.new_db_config['user'],
                    password=self.new_db_config['password'],
                    port=self.new_db_config['port'],
                    database=self.new_db_config['database']  # 确保连接到正确的数据库
                )
            return conn
        except Exception as e:
            print(f"连接数据库失败，错误信息: {e}")
            return

    def update_database(self):
        """
        将旧数据库导出的mysqldump文件传输到新数据库，会改变结构
        :return:
        """

        # 连接旧数据库并备份结构和数据，不包含存储过程和函数
        try:
            dump_cmd = f"mysqldump -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} > {self.old_db_dump_file}"
            with open(os.devnull, 'w') as devnull:
                subprocess.call(dump_cmd, shell=True, stderr=devnull)
            print(f"旧服务器数据库备份成功，备份文件路径：{self.old_db_dump_file}")
        except Exception as e:
            print(f"旧服务器数据库备份失败，错误信息:{e}")
            return

        # 备份新服务器数据库
        try:
            backup_cmd = f"mysqldump -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} > {self.new_db_backup_file}"
            with open(os.devnull, 'w') as devnull:
                subprocess.call(backup_cmd, shell=True, stderr=devnull)
            print(f"新服务器数据库备份成功，备份文件路径：{self.new_db_backup_file}")
        except Exception as e:
            print(f"新服务器数据库备份失败，错误信息:{e}")
            return

        # 两个服务器得数据都备份成功后，通过脚本补齐旧服务器数据库结构并dump下来备用
        try:
            fix_cmd = f"mysql --default-character-set=utf8mb4 -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} < {self.db_structure_fix_file}"
            with open(os.devnull, 'w') as devnull:
                subprocess.call(fix_cmd, shell=True, stderr=devnull)
            print(f"旧服务器数据库结构修正完成！")

            # 修正完成后，将修正后的数据库dump下来
            try:
                dump_cmd = f"mysqldump -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} > {self.old_db_fixed_dump_file}"
                with open(os.devnull, 'w') as devnull:
                    subprocess.call(dump_cmd, shell=True, stderr=devnull)
                print(f"修复结构后的服务器数据库下载成功，路径:{self.old_db_fixed_dump_file}，开始传输数据！")
            except Exception as e:
                print(f"旧服务器数据库备份失败，错误信息:{e}")
                return

        except Exception as e:
            print(f"旧服务器数据库结构修正失败，错误信息:{e}")
            return

        # 连接新服务器数据库并传输数据
        try:
            import_cmd = f"mysql -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} < {self.old_db_fixed_dump_file}"
            with open(os.devnull, 'w') as devnull:
                subprocess.call(import_cmd, shell=True, stderr=devnull)
        except Exception as e:
            print(f"数据库传输失败，错误信息:{e}")
            return
        print("新旧服务器数据传输成功！")


if __name__ == '__main__':
    # 测试用！！ 清理数据库结构
    delete_database_structure()
    print("\n================================================================\n")
    # 连接数据库并更新结构
    update = UpdateDatabase(old_db_host="localhost", new_db_host='localhost')
    update.update_database()
