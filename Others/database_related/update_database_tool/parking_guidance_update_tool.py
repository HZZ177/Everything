#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/13 下午6:13
# @Author  : Heshouyi
# @File    : parking_guidance_update_tool.py
# @Software: PyCharm
# @description:

import os
import subprocess
import sys
import time

import pymysql
# from delete_database_structure import delete_database_structure


class UpdateDatabase:

    def __init__(self, old_db_host, new_db_host, old_db_name="parking_guidance", new_db_name="parking_guidance"
                 , old_db_user='root', old_db_password='Keytop:wabjtam!', new_db_user='root', new_db_password='Keytop:wabjtam!'):
        self.old_database_host = old_db_host
        self.new_database_host = new_db_host
        self.old_database_name = old_db_name
        self.new_database_name = new_db_name
        self.old_db_user = old_db_user
        self.old_db_password = old_db_password
        self.new_db_user = new_db_user
        self.new_db_password = new_db_password

        # 旧数据库配置
        self.old_db_config = {
            'host': self.old_database_host,
            'port': 5831,
            'user': self.old_db_user,
            'password': self.old_db_password,
            'database': self.old_database_name,
            'charset': 'utf8mb4'
        }

        # 新数据库配置
        self.new_db_config = {
            'host': self.new_database_host,
            'port': 5831,
            'user': self.new_db_user,
            'password': self.new_db_password,
            'database': self.new_database_name,
            'charset': 'utf8mb4'
        }

        # 各种路径，使用绝对路径
        # 获取项目路径，兼容打包后的临时路径
        if getattr(sys, 'frozen', False):
            # 如果应用程序是被打包成可执行文件
            self.project_path = sys._MEIPASS    # 解压后的临时路径
            self.exe_path = os.path.dirname(sys.executable)     # exe本体所在路径
        else:
            # 如果应用程序直接运行
            self.project_path = os.path.dirname(os.path.abspath(__file__))  # 解压后的临时路径
            self.exe_path = os.path.dirname(os.path.abspath(__file__))      # exe本体所在路径

        self.project_data_path = os.path.join(self.project_path, 'data')
        self.exe_data_path = os.path.join(self.exe_path, 'data')
        if not os.path.exists(self.exe_data_path):
            os.makedirs(self.exe_data_path)
        self.mysqldump_path = os.path.join(self.project_data_path, 'mysqldump.exe')
        self.mysql_path = os.path.join(self.project_data_path, 'mysql.exe')
        self.old_db_dump_file = os.path.join(self.exe_data_path, f'old_db_backup_file_{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.sql')
        self.old_db_fixed_dump_file = os.path.join(self.exe_data_path, f'old_db_fixed_file_{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.sql')
        self.new_db_backup_file = os.path.join(self.exe_data_path, f'new_db_backup_file_{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.sql')
        self.db_structure_fix_file = os.path.join(self.project_data_path, 'parking_guidance_database_structure_fix.sql')

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

    @staticmethod
    def execute_cmd(cmd, log_message):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process

    def update_database(self, log_callback=None):
        """
        将旧数据库导出的mysqldump文件传输到新数据库，会改变结构
        :return:
        """

        def log_message(message):
            if log_callback:
                log_callback(message)
            else:
                print(message)

        # now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_message("=================开始执行数据库升级=================")
        # 连接旧数据库并备份结构和数据，不包含存储过程和函数
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行旧服务器数据库备份......")
            print(self.old_db_dump_file)
            dump_cmd = f"{self.mysqldump_path} --default-character-set=utf8mb4 -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} > {self.old_db_dump_file}"
            process = self.execute_cmd(dump_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库备份成功，备份文件路径：{self.old_db_dump_file}")
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库备份失败！错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
            return

        # 备份新服务器数据库
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行新服务器数据库备份......")
            backup_cmd = f"{self.mysqldump_path} -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} > {self.new_db_backup_file}"
            process = self.execute_cmd(backup_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 新服务器数据库备份成功，备份文件路径：{self.new_db_backup_file}")
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 新服务器数据库备份失败，错误信息:\n{e}n{stderr}\n\n升级已中断！！！")
            return

        # 两个服务器得数据都备份成功后，通过脚本补齐旧服务器数据库结构并dump下来备用
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行旧服务器数据库结构修正......")
            fix_cmd = f"{self.mysql_path} -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} < {self.db_structure_fix_file}"
            process = self.execute_cmd(fix_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库结构修正成功！")
                    # 修正完成后，将修正后的数据库dump下来
                    try:
                        log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行修正后服务器数据库下载......")
                        dump_cmd = f"{self.mysqldump_path} -h {self.old_db_config['host']} -P {self.old_db_config['port']} -u {self.old_db_config['user']} -p{self.old_db_config['password']} {self.old_db_config['database']} > {self.old_db_fixed_dump_file}"
                        process = self.execute_cmd(dump_cmd, log_message)
                        stdout, stderr = process.communicate()
                        if process.returncode == 0:
                            if "ERROR" in stdout.decode() or "error" in stdout.decode():
                                log_message(stdout.decode())
                                raise Exception(stderr.decode())
                            else:
                                log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 修正后的旧服务器数据库下载成功，备份文件路径：{self.old_db_fixed_dump_file}")
                        else:
                            raise Exception(stderr.decode())
                    except Exception as e:
                        log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 修正后的旧服务器数据库下载失败，错误信息:\n{e}n{stderr}\n\n升级已中断！！！")
                        return
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库结构修正失败，错误信息:\n{e}n{stderr}\n\n升级已中断！！！")
            return

        # 连接新服务器数据库并传输数据
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行数据库升级，正在传输数据......")
            import_cmd = f"{self.mysql_path} -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} < {self.old_db_fixed_dump_file}"
            process = self.execute_cmd(import_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 数据传输成功！\n\n寻车服务器升级完成！！！")
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 数据传输失败！，错误信息:\n{e}n{stderr}\n\n升级已中断！！！")
            return


if __name__ == '__main__':
    # 测试用！！ 清理数据库结构
    #delete_database_structure()
    print("\n================================================================\n")

    # 连接数据库并更新结构
    update = UpdateDatabase(old_db_host="localhost", new_db_host='localhost')
    update.update_database()
