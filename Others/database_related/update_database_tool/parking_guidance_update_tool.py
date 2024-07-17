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
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 新服务器数据库备份失败，错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
            return

        # 先清理表b_car_in_out_record和表b_recognition_record的历史数据
        connection = None
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行旧服务器数据库大表清理......")
            connection = self.connect_database('old')
            with connection.cursor() as cursor:
                truncate_sqls = [
                    "TRUNCATE TABLE b_car_in_out_record;",
                    "TRUNCATE TABLE b_recognition_record;"
                ]
                for sql in truncate_sqls:
                    cursor.execute(sql)
                connection.commit()
                log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库大表清理成功！")
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Warning- {e}")
        finally:
            connection.close()

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
                        log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 修正后的旧服务器数据库下载失败，错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
                        return
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 旧服务器数据库结构修正失败，错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
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
                    log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 数据传输成功！")

                    # 执行truncate和insert语句
                    connection = None
                    try:
                        connection = self.connect_database('new')
                        with connection.cursor() as cursor:
                            log_message(
                                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始初始化config配置表......")

                            truncate_sqls = [
                                "TRUNCATE TABLE f_config;",
                                "TRUNCATE TABLE ini_config;",
                                "TRUNCATE TABLE schedule_config;",
                                "TRUNCATE TABLE t_access_config;"
                            ]
                            insert_sqls = [
                                "INSERT INTO `ini_config` (`id`, `dsp_recog`, `witch`, `comname`, `ret`, `province`, `pic_switch`, `creator`, `create_time`, `updater`, `update_time`) VALUES (1, 0, 1, 'COM3', 0, NULL, 0, NULL, NULL, NULL, '2024-01-25 10:53:13');",
                                "INSERT INTO `schedule_config` (`id`, `create_time`, `update_time`, `park_img_duration`, `area_park_img_duration`, `in_car_push_switch`, `out_car_push_switch`, `update_plate_push_switch`, `empty_park_push_switch`, `empty_park_push_lot`, `empty_park_push_url`, `park_change_push_switch`, `park_change_push_lot`, `park_change_push_url`, `creator`, `url_prefix_config`, `free_space_num_switch`, `image_upload_switch`, `unified_image_prefix`, `post_bus_in_out`, `post_node_device_status`, `clean_stereoscopic_park_switch`, `free_space_switch`, `post_node_device_url`, `clean_stereoscopic_park_duration`, `car_loc_info_switch`, `area_push_switch`, `tank_warn_push_switch`, `light_scheme_duration`, `grpc_switch`, `screen_cmd_interval`, `screen_cmd_interval_fast`, `statistic_screen_type`, `query_recognize_record`, `plate_match_rule`, `clean_temp_picture`, `clean_recognition_table`, `clean_area_picture`, `warn_switch`) VALUES (1, NULL, '2024-02-07 14:10:30', 30, 1, 0, 1, 0, 1, NULL, NULL, 1, NULL, NULL, NULL, 'http://localhost:8083', 1, 0, 'http://localhost:8083', 1, 1, 1, 1, NULL, 30, 1, 1, 1, 60, 1, 30, 8, 1, 0, 1, 1, 30, 1, 1)",
                                "INSERT INTO `t_access_config` (`id`, `dsp_port`, `node_port`, `ip_Pre`, `broadcast_times`, `broadcast_interval`, `channel_http`, `serial_port`, `baud_rate`, `A`, `B`, `C`, `pr_num`, `army_car`, `police_car`, `wujing_car`, `farm_car`, `embassy_car`, `personality_car`, `civil_car`, `new_energy_car`, `type_pr_num`, `set_lr_num`, `set_lpr_cs`, `province`, `set_priority`, `original_picture_path`, `front_save_path`, `temp_rcv_path`, `recognition_path`, `recognition_lib_path`, `switch_serial_port`, `region_picture_path`, `snap_picture_path`, `quality_inspection_picture_path`, `recognition_switch`, `free_occupy_switch`) VALUES (1, 7799, 7777, '172.10', 3, 5, 'http://127.0.0.1:7072', '/dev/ttyS0', 9600, 1, 1, 1, 9, 1, 1, 0, 1, 1, 1, 1, 1, 9, 2, 1, '川', 0, '/home/findcar/FindCarServer/original', '/home/findcar/ParkingGuidance/carImage', '/home/findcar/FindCarServer/temp', '/home/findcar/FindCarServer/recognition', '/home/findcar/FindCarServer/lib/', 0, '/home/findcar/ParkingGuidance/snappedImage', '/home/findcar/ParkingGuidance/carImage/snap', '/home/findcar/FindCarServer/qualityInspectionCenter', 0, 0);",
                                "INSERT INTO `f_config` (`id`, `config_code`, `config_value`, `config_desc`, `attribute`, `deleted`, `create_time`, `creator`, `update_time`, `updater`, `aws_enable_switch`, `guidance_swagger_switch`, `channel_swagger_switch`) VALUES (1, 'tanker_expel_switch', '1', '油车违停告警开关', '', 0, '2024-01-25 10:53:13', '系统管理员', '2024-01-25 10:53:13', '系统管理员', 0, 0, 0);"
                            ]
                            alter_sqls = [
                                "ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                            ]

                            for sql in truncate_sqls:
                                cursor.execute(sql)
                            for sql in insert_sqls:
                                cursor.execute(sql)
                            for sql in alter_sqls:
                                cursor.execute(sql)

                            connection.commit()
                            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 初始化config配置表成功！\n\n寻车服务器升级完成！！！")
                    except Exception as e:
                        log_message(
                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 初始化config配置表失败，错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
                    finally:
                        connection.close()
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 数据传输失败！，错误信息:\n{e}]\n{stderr}\n\n升级已中断！！！")
            return


if __name__ == '__main__':
    # 测试用！！ 清理数据库结构
    # delete_database_structure()
    print("\n================================================================\n")

    # 连接数据库并更新结构
    update = UpdateDatabase(old_db_host="localhost", new_db_host='localhost')
    update.update_database()
