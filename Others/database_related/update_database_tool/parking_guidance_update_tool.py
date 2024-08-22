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

    def __init__(self, old_db_host, new_db_host, old_db_name="parking_guidance", new_db_name="parking_guidance_3.2.3"
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
        self.new_db_internation_backup_file = os.path.join(self.exe_data_path, f'new_db_internation_backup_file_{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}.sql')
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

        # 备份新服务器国际化表
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始备份国际化......")
            backup_internationalization_cmd = f"{self.mysqldump_path} -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} internationalization> {self.new_db_internation_backup_file}"
            process = self.execute_cmd(backup_internationalization_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(
                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 国际化备份成功，备份文件路径：{self.new_db_internation_backup_file}")
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(
                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 国际化备份失败，错误信息:\n{e}\n{stderr}\n\n升级已中断！！！")
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

            # 修改旧表字符防止备份汉字乱码
            connection = self.connect_database('old')
            with connection.cursor() as cursor:

                fix_sqls = [
                    "ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                ]
                for sql in fix_sqls:
                    cursor.execute(sql)


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

                            drop_sqls = [
                                "Drop TABLE f_config;",
                                "Drop TABLE ini_config;",
                                "Drop TABLE schedule_config;",
                                "Drop TABLE t_access_config;"
                            ]

                            create_sqls = [
                                """
CREATE TABLE IF NOT EXISTS `schedule_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `create_time` datetime DEFAULT NULL COMMENT '更新时间',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `park_img_duration` int(11) DEFAULT NULL COMMENT '车位照片定时清理',
  `area_park_img_duration` int(11) DEFAULT NULL COMMENT '区域在场车辆定时清理',
  `in_car_push_switch` tinyint(1) DEFAULT '0' COMMENT '车位入车延迟上报，0开启，1关闭',
  `out_car_push_switch` tinyint(1) DEFAULT '0' COMMENT '车位出车延迟上报，0开启，1关闭',
  `update_plate_push_switch` tinyint(1) DEFAULT '1' COMMENT '更新车牌上报，0开启，1关闭',
  `empty_park_push_switch` tinyint(1) DEFAULT NULL COMMENT '空车位上报，0开启，1关闭',
  `empty_park_push_lot` varchar(255) DEFAULT NULL COMMENT '空车位上报车场id',
  `empty_park_push_url` varchar(2000) DEFAULT NULL COMMENT '空车位上报url  多个url直接用英语逗号隔开',
  `park_change_push_switch` tinyint(1) DEFAULT NULL COMMENT '车位状态变更上报',
  `park_change_push_lot` varchar(255) DEFAULT NULL COMMENT '车位状态变更上报车场id',
  `park_change_push_url` varchar(2000) DEFAULT NULL COMMENT '车位状态变更上报url  多个url直接用英语逗号隔开',
  `creator` varchar(255) DEFAULT NULL COMMENT '更新者',
  `url_prefix_config` varchar(255) DEFAULT NULL COMMENT '单车场查询返回图片URL拼接前缀地址',
  `free_space_num_switch` tinyint(1) DEFAULT '1' COMMENT '实时剩余车位数本地文件对接开关，0开启，1关闭',
  `image_upload_switch` tinyint(1) DEFAULT '0' COMMENT '图片上传OSS开关(0:开启,1:关闭)',
  `unified_image_prefix` varchar(255) DEFAULT NULL COMMENT '统一接口查询返回图片URL前缀',
  `post_bus_in_out` tinyint(1) DEFAULT '1' COMMENT '上报出入车 0:开启  1:关闭',
  `post_node_device_status` tinyint(1) DEFAULT '1' COMMENT '节点设备状态变更上报 0:开启  1:关闭',
  `clean_stereoscopic_park_switch` tinyint(1) DEFAULT '1' COMMENT '定时清理立体车位的车牌识别记录 0:开启  1:关闭',
  `free_space_switch` tinyint(1) DEFAULT '1' COMMENT '剩余车位数上报收费系统开关 0:开启  1:关闭',
  `post_node_device_url` varchar(2000) DEFAULT NULL COMMENT '节点设备状态变更上报url  多个url直接用英语逗号隔开',
  `clean_stereoscopic_park_duration` int(11) DEFAULT NULL COMMENT '清理立体车位的车牌识别记录(天)',
  `car_loc_info_switch` tinyint(1) DEFAULT '1' COMMENT '车辆停放位置查询接口开关 0:开启  1:关闭',
  `area_push_switch` tinyint(1) DEFAULT '1' COMMENT '区域进出车上报开关 0:开启  1:关闭',
  `tank_warn_push_switch` tinyint(1) DEFAULT '1' COMMENT '油车告警上报开关 0:开启  1:关闭',
  `light_scheme_duration` int(11) DEFAULT '60' COMMENT '车位灯方案删除 ',
  `grpc_switch` tinyint(1) DEFAULT '1' COMMENT 'gRPC连接云端C++用于统一接口开关 0:开启  1:关闭',
  `screen_cmd_interval` int(11) DEFAULT '30' COMMENT '屏指令下发间隔时间（低频），默认30分钟',
  `screen_cmd_interval_fast` int(11) NOT NULL DEFAULT '8' COMMENT '屏指令下发间隔时间（高频），默认8秒钟',
  `statistic_screen_type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '统计屏数据方式  0=定时统计 1=进出车触发 ',
  `query_recognize_record` tinyint(1) DEFAULT '0' COMMENT '是否查询识别记录 0:开启  1:关闭（开启查询识别记录，关闭查询实时在场车）',
  `plate_match_rule` int(11) DEFAULT '1' COMMENT '车牌匹配规则（0 【完全匹配】只返回除汉字部分完全一致的车牌）;1 【全匹配】 查2222可能返回12222或22221',
  `clean_temp_picture` int(11) DEFAULT '1' COMMENT '清理n天以前的临时识别文件',
  `clean_recognition_table` int(11) DEFAULT '30' COMMENT '车牌识别日志表定时清理（单位：天）',
  `clean_area_picture` int(11) DEFAULT '1' COMMENT '区域照片文件定时清理（单位：天）',
  `warn_switch` int(11) NOT NULL DEFAULT '1' COMMENT '告警开关 1=开 0=关',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='参数配置表';
                                """,
                                """
CREATE TABLE IF NOT EXISTS `f_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `config_code` varchar(64) DEFAULT '' COMMENT '配置编码',
  `config_value` varchar(64) DEFAULT '' COMMENT '配置值',
  `config_desc` varchar(255) DEFAULT '' COMMENT '配置描述',
  `attribute` varchar(64) DEFAULT '' COMMENT '额外字段',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除（0：未删除，1：已删除）',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `aws_enable_switch` tinyint(1) DEFAULT '1' COMMENT '是否上传车场问题图片到ai中心 0:开启  1:关闭',
  `guidance_swagger_switch` tinyint(1) DEFAULT '1' COMMENT 'parking_guidance服务swagger配置开关 0:开启  1:关闭',
  `channel_swagger_switch` tinyint(1) DEFAULT '1' COMMENT 'channel_service服务swagger配置开关 0:开启  1:关闭',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_config_code` (`config_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='系统配置表';
                                """,
                                """
CREATE TABLE IF NOT EXISTS `ini_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `dsp_recog` tinyint(1) DEFAULT '0' COMMENT '控制软识别与硬识别 0 软识别, 1 硬识别',
  `witch` tinyint(1) DEFAULT '0' COMMENT '控制故障状态的设备的开关 0 关闭， 1 开启',
  `comname` varchar(255) DEFAULT NULL COMMENT '连接服务器的端口号 windows下是COM5, linux下是 /dev/ttyS0',
  `ret` tinyint(1) DEFAULT '0' COMMENT '控制TCP还是485通讯 0 tcp, 1 485',
  `province` varchar(255) DEFAULT NULL COMMENT '车牌的默认省份(省份简称汉字) 默认为空',
  `pic_switch` tinyint(1) DEFAULT '0' COMMENT '是否开启空车牌图片收集功能  1 开启,  0 关闭',
  `creator` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updater` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=DYNAMIC COMMENT='C++参数配置表';
                                """,
                                """
CREATE TABLE IF NOT EXISTS `t_access_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '唯一id',
  `dsp_port` int(11) DEFAULT NULL COMMENT 'dsp 连接端口',
  `node_port` int(11) DEFAULT NULL COMMENT 'node tcp节点连接端口',
  `ip_Pre` varchar(255) DEFAULT NULL COMMENT 'tcp地址拼接前缀',
  `broadcast_times` int(11) DEFAULT NULL COMMENT '广播次数',
  `broadcast_interval` int(11) DEFAULT NULL COMMENT '播放间隔',
  `channel_http` varchar(255) DEFAULT NULL COMMENT 'channel服务url地址',
  `serial_port` varchar(64) DEFAULT NULL COMMENT '串口地址',
  `baud_rate` int(11) DEFAULT NULL COMMENT '波特率',
  `A` int(11) DEFAULT NULL COMMENT '识别模式A',
  `B` int(11) DEFAULT NULL COMMENT '识别模式B',
  `C` int(11) DEFAULT NULL COMMENT '识别模式C',
  `pr_num` int(11) DEFAULT NULL COMMENT '车牌类型长度',
  `army_car` int(11) DEFAULT NULL COMMENT '军车车牌',
  `police_car` int(11) DEFAULT NULL COMMENT '警车车牌',
  `wujing_car` int(11) DEFAULT NULL COMMENT '武警车牌',
  `farm_car` int(11) DEFAULT NULL COMMENT '农用车牌',
  `embassy_car` int(11) DEFAULT NULL COMMENT '大使馆车牌',
  `personality_car` int(11) DEFAULT NULL COMMENT '个性化车牌',
  `civil_car` int(11) DEFAULT NULL COMMENT '民航车牌',
  `new_energy_car` int(11) DEFAULT NULL COMMENT '新能源车牌',
  `type_pr_num` int(11) DEFAULT NULL COMMENT '车牌长度',
  `set_lr_num` int(11) DEFAULT NULL COMMENT '车牌数组长度',
  `set_lpr_cs` int(11) DEFAULT NULL COMMENT '识别种类（0:裁剪，1：A版，2：B版，3：A+B版，4：C版 5：A+C版，6：B+C，7：A+B+C）',
  `province` varchar(12) DEFAULT NULL COMMENT '默认省份',
  `set_priority` int(11) DEFAULT '0' COMMENT '设置三地车牌输出优先级:1:MO 2:HK 3:CN 4:CN>HK>MO 5:MO>CN>HK 6:MO>HK>CN 7:HK>CN>MO 8:HK>MO>CN other:CN>MO>HK',
  `original_picture_path` varchar(255) DEFAULT NULL COMMENT '原图保存路径',
  `front_save_path` varchar(255) DEFAULT NULL COMMENT '前端保存路径',
  `temp_rcv_path` varchar(255) DEFAULT NULL COMMENT '临时文件路径',
  `recognition_path` varchar(255) DEFAULT NULL COMMENT '识别文件路径',
  `recognition_lib_path` varchar(255) DEFAULT NULL COMMENT '识别库地址',
  `switch_serial_port` tinyint(1) DEFAULT '1' COMMENT '485节点串口扫描开关（0：关闭  1：开启）',
  `region_picture_path` varchar(255) DEFAULT NULL COMMENT '区域相机照片保存路径',
  `snap_picture_path` varchar(255) DEFAULT NULL COMMENT '相机抓拍照片保存路径',
  `quality_inspection_picture_path` varchar(255) DEFAULT NULL COMMENT '质检中心抓拍照片保存路径',
  `recognition_switch` tinyint(1) DEFAULT '1' COMMENT '识别库开关，0:关闭 1:开启',
  `free_occupy_switch` tinyint(1) DEFAULT '0' COMMENT '找车系统-有车 和找车系统-无车数据接口上报开关 (0：关闭，1：开启)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 AVG_ROW_LENGTH=16384 ROW_FORMAT=COMPACT COMMENT='C++重构配置信息表';
                                """
                            ]

                            insert_sqls = [
                                "INSERT INTO `ini_config` (`id`, `dsp_recog`, `witch`, `comname`, `ret`, `province`, `pic_switch`, `creator`, `create_time`, `updater`, `update_time`) VALUES (1, 0, 1, 'COM3', 0, NULL, 0, NULL, NULL, NULL, '2024-01-25 10:53:13');",
                                "INSERT INTO `schedule_config` (`id`, `create_time`, `update_time`, `park_img_duration`, `area_park_img_duration`, `in_car_push_switch`, `out_car_push_switch`, `update_plate_push_switch`, `empty_park_push_switch`, `empty_park_push_lot`, `empty_park_push_url`, `park_change_push_switch`, `park_change_push_lot`, `park_change_push_url`, `creator`, `url_prefix_config`, `free_space_num_switch`, `image_upload_switch`, `unified_image_prefix`, `post_bus_in_out`, `post_node_device_status`, `clean_stereoscopic_park_switch`, `free_space_switch`, `post_node_device_url`, `clean_stereoscopic_park_duration`, `car_loc_info_switch`, `area_push_switch`, `tank_warn_push_switch`, `light_scheme_duration`, `grpc_switch`, `screen_cmd_interval`, `screen_cmd_interval_fast`, `statistic_screen_type`, `query_recognize_record`, `plate_match_rule`, `clean_temp_picture`, `clean_recognition_table`, `clean_area_picture`, `warn_switch`) VALUES (1, NULL, '2024-02-07 14:10:30', 30, 1, 0, 1, 0, 1, NULL, NULL, 1, NULL, NULL, NULL, 'http://localhost:8083', 1, 0, 'http://localhost:8083', 1, 1, 1, 1, NULL, 30, 1, 1, 1, 60, 1, 30, 8, 1, 0, 1, 1, 30, 1, 1)",
                                "INSERT INTO `t_access_config` (`id`, `dsp_port`, `node_port`, `ip_Pre`, `broadcast_times`, `broadcast_interval`, `channel_http`, `serial_port`, `baud_rate`, `A`, `B`, `C`, `pr_num`, `army_car`, `police_car`, `wujing_car`, `farm_car`, `embassy_car`, `personality_car`, `civil_car`, `new_energy_car`, `type_pr_num`, `set_lr_num`, `set_lpr_cs`, `province`, `set_priority`, `original_picture_path`, `front_save_path`, `temp_rcv_path`, `recognition_path`, `recognition_lib_path`, `switch_serial_port`, `region_picture_path`, `snap_picture_path`, `quality_inspection_picture_path`, `recognition_switch`, `free_occupy_switch`) VALUES (1, 7799, 7777, '172.10', 3, 5, 'http://127.0.0.1:7072', '/dev/ttyS0', 9600, 1, 1, 1, 9, 1, 1, 0, 1, 1, 1, 1, 1, 9, 2, 1, '川', 0, '/home/findCarApi/FindCarServer/original', '/home/findCarApi/ParkingGuidance/carImage', '/home/findCarApi/FindCarServer/temp', '/home/findCarApi/FindCarServer/recognition', '/home/findCarApi/FindCarServer/lib/', 0, '/home/findCarApi/ParkingGuidance/snappedImage', '/home/findCarApi/ParkingGuidance/carImage/snap', '/home/findCarApi/FindCarServer/qualityInspectionCenter', 0, 0);",
                                "INSERT INTO `f_config` (`id`, `config_code`, `config_value`, `config_desc`, `attribute`, `deleted`, `create_time`, `creator`, `update_time`, `updater`, `aws_enable_switch`, `guidance_swagger_switch`, `channel_swagger_switch`) VALUES (1, 'tanker_expel_switch', '1', '油车违停告警开关', '', 0, '2024-01-25 10:53:13', '系统管理员', '2024-01-25 10:53:13', '系统管理员', 0, 0, 0);"
                            ]
                            alter_sqls = [
                                "ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                            ]

                            for sql in drop_sqls:
                                cursor.execute(sql)
                            for sql in create_sqls:
                                cursor.execute(sql)
                            for sql in insert_sqls:
                                cursor.execute(sql)
                            for sql in alter_sqls:
                                cursor.execute(sql)

                            connection.commit()
                            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 初始化config配置表成功！")
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

        # 重置国际化
        try:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 开始进行国际化覆盖......")
            internation_cmd = f"{self.mysql_path} -h {self.new_db_config['host']} -P {self.new_db_config['port']} -u {self.new_db_config['user']} -p{self.new_db_config['password']} {self.new_db_config['database']} < {self.new_db_internation_backup_file}"
            process = self.execute_cmd(internation_cmd, log_message)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                if "ERROR" in stdout.decode() or "error" in stdout.decode():
                    log_message(stdout.decode())
                    raise Exception(stderr.decode())
                else:
                    log_message(
                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 国际化覆盖成功")
            else:
                raise Exception(stderr.decode())
        except Exception as e:
            log_message(
                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 新服务器数据库备份失败，错误信息:\n{e}\n{stderr}\n\n请升级完成后手动检查国际化表")

        # 给lot_info表新增临时到期时间-lisence_trial_period
        update_sql = 'UPDATE lot_info SET lisence_trial_period = IF(lisence_trial_period IS NULL, DATE_ADD(NOW(), INTERVAL 30 DAY), lisence_trial_period) WHERE id = 1;'
        try:
            connection = self.connect_database('new')
            with connection.cursor() as cursor:
                affected_rows = cursor.execute(update_sql)
                connection.commit()  # 提交事务
                log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} lot_info表更新临时到期时间成功, 影响的行数: {affected_rows}\n\n寻车服务器升级完成！！！")
        except Exception as e:
            log_message(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 更新lot_info表临时到期时间失败，错误信息:\n{e}\n{stderr}\n\n请升级完成后手动检查lot_info表到期时间")


if __name__ == '__main__':
    # 测试用！！ 清理数据库结构
    # delete_database_structure()
    print("\n================================================================\n")

    # 连接数据库并更新结构
    update = UpdateDatabase(old_db_host="localhost", new_db_host='localhost')
    update.update_database()
