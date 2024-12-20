import os
import queue
import re
import sys
import threading
from collections import defaultdict
from datetime import datetime
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pack_with_pyinstaller import version


class Application:
    """动态生成修复sql文件的核心功能工具类"""

    def __init__(
            self,
            base_host, base_port, base_user, base_password, base_database,
            target_host, target_port, target_user, target_password, target_database,
            log
    ):
        # 基线库相关参数
        self.base_host = base_host
        self.base_port = base_port
        self.base_user = base_user
        self.base_password = base_password
        self.base_database = base_database

        # 修复目标库相关参数
        self.target_host = target_host
        self.target_port = target_port
        self.target_user = target_user
        self.target_password = target_password
        self.target_database = target_database

        self.base_connection = None  # 基线库连接对象
        self.target_connection = None  # 修复目标库连接对象
        self.log = log  # 日志输出更新函数

    def log_message(self, message):
        """用于输出日志到UI日志控件"""
        if self.log:
            self.log(message)

    def connect_to_base_database(self):
        """连接到基线库"""
        try:
            self.base_connection = pymysql.connect(
                host=self.base_host,
                user=self.base_user,
                password=self.base_password,
                database=self.base_database,
                port=self.base_port,
                connect_timeout=10,
                read_timeout=10
            )
        except Exception as e:
            self.log_message(f"基线库连接失败: {e}")
            raise e

    def connect_to_target_database(self):
        """连接到目标库"""
        try:
            self.target_connection = pymysql.connect(
                host=self.target_host,
                user=self.target_user,
                password=self.target_password,
                database=self.target_database,
                port=self.target_port,
                connect_timeout=10,
                read_timeout=10
            )
        except Exception as e:
            self.log_message(f"修复目标库连接失败: {e}")
            raise e

    def disconnect_dbs(self):
        try:
            if self.base_connection:
                self.base_connection.close()
            if self.target_connection:
                self.target_connection.close()
        except Exception as e:
            self.log_message(f"关闭数据库连接失败: {e}")
            raise e

    def insert_procedure_sentences(self):
        """写入存储过程"""
        self.log_message("开始对目标库新增存储过程......")

        clear_procedure = "DROP PROCEDURE IF EXISTS add_element_unless_exists;"

        procedure_add_element_unless_exists = """
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

END;
"""
        try:
            with self.target_connection.cursor() as cursor:
                self.log_message(f"清理存储过程\n{clear_procedure}")
                cursor.execute(clear_procedure)  # 清除之前存在的存储过程

                self.log_message(f"写入存储过程\n{procedure_add_element_unless_exists}")
                cursor.execute(procedure_add_element_unless_exists)  # 写入存储过程
                self.target_connection.commit()  # 手动提交防止自动提交模式被关闭

            self.log_message("存储过程写入成功！")
        except Exception as e:
            self.log_message(f"存储过程写入失败: {e}")
            raise e

    def get_all_construct_sentences(self):
        """从基线库获取所有表创建语句，动态生成后执行到目标库"""
        self.log_message("开始获取基线库表结构并动态生成......")

        try:  # 从基线库获取所有表名
            with self.base_connection.cursor() as cursor:
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                self.log_message("-- ===============全量创建标准库表===============\n")
                for table in tables:
                    table_name = table[0]
                    self.log_message(f"-- 构造表 {table_name}\n")

                    # 获取所有表的初始化语句
                    cursor.execute(f"show create TABLE `{table_name}`")
                    columns = cursor.fetchall()

                    for column in columns:
                        describe = column[1]
                        crate_sql = f"CREATE TABLE IF NOT EXISTS{str(describe).replace('CREATE TABLE', '')};\n"

                        self.log_message(crate_sql)  # 打印
                        # 对目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(crate_sql)  # 执行
                        self.target_connection.commit()  # 提交

            self.log_message("动态构建表结构并执行成功！")
        except Exception as e:
            self.log_message(f"构建并执行建表语句失败: {e}")
            raise e

    def init_config_tables(self):
        try:  # 从基线库获取所有表名
            with self.target_connection.cursor() as cursor:
                cursor.execute("select * from ini_config")
                result = cursor.fetchone()
                # 如果查询结果为空，执行初始化语句新增基础值
                if result is None:
                    self.log_message("检测到ini_config表没有任何值，新增默认值")
                    cursor.execute("INSERT INTO `ini_config` (`id`, `dsp_recog`, `witch`, `comname`, `ret`, `province`, `pic_switch`, `creator`, `create_time`, `updater`, `update_time`) VALUES (1, 0, 1, 'COM3', 0, NULL, 0, NULL, NULL, NULL, '2024-01-25 10:53:13');",)

                cursor.execute("select * from schedule_config")
                # 如果查询结果为空，执行初始化语句新增基础值
                if cursor.fetchone() is None:
                    self.log_message("检测到schedule_config表没有任何值，新增默认值")
                    cursor.execute("INSERT INTO `schedule_config` (`id`, `create_time`, `update_time`, `park_img_duration`, `area_park_img_duration`, `in_car_push_switch`, `out_car_push_switch`, `update_plate_push_switch`, `empty_park_push_switch`, `empty_park_push_lot`, `empty_park_push_url`, `park_change_push_switch`, `park_change_push_lot`, `park_change_push_url`, `creator`, `url_prefix_config`, `free_space_num_switch`, `image_upload_switch`, `unified_image_prefix`, `post_bus_in_out`, `post_node_device_status`, `clean_stereoscopic_park_switch`, `free_space_switch`, `post_node_device_url`, `clean_stereoscopic_park_duration`, `car_loc_info_switch`, `area_push_switch`, `tank_warn_push_switch`, `light_scheme_duration`, `grpc_switch`, `screen_cmd_interval`, `screen_cmd_interval_fast`, `statistic_screen_type`, `query_recognize_record`, `plate_match_rule`, `clean_temp_picture`, `clean_recognition_table`, `clean_area_picture`, `warn_switch`) VALUES (1, NULL, '2024-02-07 14:10:30', 30, 1, 0, 1, 0, 1, NULL, NULL, 1, NULL, NULL, NULL, 'http://localhost:8083', 1, 0, 'http://localhost:8083', 1, 1, 1, 1, NULL, 30, 1, 1, 1, 60, 1, 30, 8, 1, 0, 1, 1, 30, 1, 1)",)

                cursor.execute("select * from t_access_config")
                # 如果查询结果为空，执行初始化语句新增基础值
                if cursor.fetchone() is None:
                    self.log_message("检测到t_access_config表没有任何值，新增默认值")
                    cursor.execute("INSERT INTO `t_access_config` (`id`, `dsp_port`, `node_port`, `ip_Pre`, `broadcast_times`, `broadcast_interval`, `channel_http`, `serial_port`, `baud_rate`, `A`, `B`, `C`, `pr_num`, `army_car`, `police_car`, `wujing_car`, `farm_car`, `embassy_car`, `personality_car`, `civil_car`, `new_energy_car`, `type_pr_num`, `set_lr_num`, `set_lpr_cs`, `province`, `set_priority`, `original_picture_path`, `front_save_path`, `temp_rcv_path`, `recognition_path`, `recognition_lib_path`, `switch_serial_port`, `region_picture_path`, `snap_picture_path`, `quality_inspection_picture_path`, `recognition_switch`, `free_occupy_switch`) VALUES (1, 7799, 7777, '172.10', 3, 5, 'http://127.0.0.1:7072', '/dev/ttyS0', 9600, 1, 1, 1, 9, 1, 1, 0, 1, 1, 1, 1, 1, 9, 2, 1, '川', 0, '/home/findCarApi/FindCarServer/original', '/home/findCarApi/ParkingGuidance/carImage', '/home/findCarApi/FindCarServer/temp', '/home/findCarApi/FindCarServer/recognition', '/home/findCarApi/FindCarServer/lib/', 0, '/home/findCarApi/ParkingGuidance/snappedImage', '/home/findCarApi/ParkingGuidance/carImage/snap', '/home/findCarApi/FindCarServer/qualityInspectionCenter', 0, 0);",)

                cursor.execute("select * from f_config")
                # 如果查询结果为空，执行初始化语句新增基础值
                if cursor.fetchone() is None:
                    self.log_message("检测到f_config表没有任何值，新增默认值")
                    cursor.execute("INSERT INTO `f_config` (`id`, `config_code`, `config_value`, `config_desc`, `attribute`, `deleted`, `create_time`, `creator`, `update_time`, `updater`, `aws_enable_switch`, `guidance_swagger_switch`, `channel_swagger_switch`) VALUES (1, 'tanker_expel_switch', '1', '油车违停告警开关', '', 0, '2024-01-25 10:53:13', '系统管理员', '2024-01-25 10:53:13', '系统管理员', 0, 0, 0);")

        except Exception as e:
            self.log_message(f"有配置表没有任何值，但新增初始化数据失败: {e}")
            raise e

    def get_all_column_insert_sentences_ktpark(self):
        """ktpark获取并写入所有字段和索引创建语句"""
        self.log_message("开始获取字段和索引创建语句并写入......")

        try:  # 在基线库获取
            with self.base_connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                self.log_message("-- ===============全量更新所有表字段===============\n")
                for table in tables:
                    table_name = table[0]
                    self.log_message(f"-- 更新表 {table_name} 所有字段和索引\n")

                    # 获取表字段详细信息
                    cursor.execute(f"""SELECT
                                            COLUMN_NAME,
                                            COLUMN_TYPE,
                                            IS_NULLABLE,
                                            COLUMN_DEFAULT,
                                            COLUMN_KEY,
                                            EXTRA
                                        FROM
                                            INFORMATION_SCHEMA.COLUMNS
                                        WHERE
                                            TABLE_SCHEMA = '{self.base_database}'
                                            AND TABLE_NAME = '{table_name}';""")
                    columns = cursor.fetchall()

                    # 获取表索引详细信息
                    cursor.execute(f"""SELECT
                                            INDEX_NAME,
                                            NON_UNIQUE,
                                            INDEX_TYPE,
                                            COLUMN_NAME
                                        FROM
                                            INFORMATION_SCHEMA.STATISTICS
                                        WHERE
                                            TABLE_SCHEMA = '{self.base_database}'
                                            AND TABLE_NAME = '{table_name}';""")
                    indexes = cursor.fetchall()

                    # 初始化字段位置计数器
                    column_id = 0
                    column_pre = None  # 储存上一个字段

                    table_call_messages = ""
                    # 动态生成字段添加语句
                    for column in columns:
                        column_name, column_type, is_nullable, column_default, column_key, extra = column
                        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                        # 需要单独处理默认值为空串的情况
                        if column_default is not None:
                            if column_default == '':
                                default = "DEFAULT ''"
                            elif column_default == "2013-01-01 00:00:00" or "#" in column_default:
                                default = f"DEFAULT '{column_default}'"

                            else:
                                default = f"DEFAULT {column_default}"
                        else:
                            default = ""

                        # 单独处理附加信息里的auto_increment，变为auto_increment PRIMARY KEY
                        if extra:
                            if "auto_increment" in extra.lower():
                                extra_info = f"{extra} PRIMARY KEY"
                            else:
                                extra_info = extra
                        else:
                            extra_info = ""
                        # 动态生成 SQL 语句
                        column_definition = f"`{column_name}` {column_type} {nullable} {default} {extra_info}".strip()
                        # 转义单引号以支持 SET 类型的字段
                        escaped_definition = column_definition.replace("'", "\\'")

                        if column_id == 0:
                            call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition};');\n"
                        else:
                            call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition} AFTER `{column_pre}`;');\n"

                        table_call_messages += call_procedure_column_sql  # 打印
                        # 在目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(call_procedure_column_sql)  # 执行
                        self.target_connection.commit()  # 提交

                        column_pre = column_name
                        column_id += 1

                    # 先将索引信息按照 index_name 分组
                    index_dict = defaultdict(list)

                    for index in indexes:
                        index_name, non_unique, index_type, column_name = index
                        index_type = "UNIQUE" if non_unique == 0 else ""
                        index_dict[(index_name, index_type)].append(column_name)

                    # 遍历分组后的索引信息，生成 SQL 语句
                    for (index_name, index_type), columns in index_dict.items():
                        columns_list = ", ".join(f"`{col}`" for col in columns)
                        if index_name == "PRIMARY":
                            index_statement = f"ADD PRIMARY KEY ({columns_list})"
                        else:
                            index_statement = f"ADD {index_type} INDEX `{index_name}` ({columns_list}) USING BTREE"

                        call_procedure_index_sql = f"CALL add_element_unless_exists('index', '{table_name}', '{index_name}', 'ALTER TABLE {table_name} {index_statement};');\n"

                        table_call_messages += call_procedure_index_sql  # 打印
                        # 在目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(call_procedure_index_sql)  # 执行
                        self.target_connection.commit()  # 提交

                    self.log_message(table_call_messages)
            self.log_message("构建字段和索引创建语句并执行成功！")
        except Exception as e:
            self.log_message(f"构建字段和索引创建语句并执行失败: {e}")
            raise e

    def get_all_column_insert_sentences_parking_guidance(self):
        """parking_guidance获取并写入所有字段和索引创建语句"""
        self.log_message("开始获取字段和索引创建语句并写入......")

        try:  # 在基线库获取
            with self.base_connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                self.log_message("-- ===============全量更新所有表字段===============\n")
                for table in tables:
                    table_name = table[0]

                    # 获取所有表的初始化语句
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    create_sentences = cursor.fetchall()
                    # 去掉所有建表语句中的多行注释
                    create_sentences_without_annotation = re.sub(r'/\*.*?\*/', '', str(create_sentences), flags=re.S)
                    fields = str(create_sentences_without_annotation).split(r'\n')[1:][:-1]

                    # 获取所有的表级别注释
                    cursor.execute(f"SHOW TABLE STATUS LIKE '{table_name}'")
                    table_status = cursor.fetchone()
                    table_comment = table_status[17] if table_status else None

                    # 使用正则表达式单独分组COMMENT之前和之后的内容，方便分开处理格式规范
                    processed_fields = []
                    comments = []
                    table_call_messages = ""
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
                    self.log_message(f"-- 更新表 {table_name} 所有字段和索引\n")
                    # file.write(f"ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;\n")
                    comment_sentence = f"ALTER TABLE {table_name} COMMENT = '{table_comment}';\n"
                    format_sentences = f"ALTER TABLE {table_name} ROW_FORMAT=DYNAMIC;\n"
                    table_call_messages += comment_sentence + format_sentences

                    with self.target_connection.cursor() as cursor_target:
                        cursor_target.execute(comment_sentence)
                        cursor_target.execute(format_sentences)

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
                                call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_now}', 'ALTER TABLE {table_name} ADD COLUMN {final_sentence};');\n"
                            else:
                                call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_now}', 'ALTER TABLE {table_name} ADD COLUMN {final_sentence} AFTER {column_pre};');\n"
                            table_call_messages += call_procedure_column_sql
                            with self.target_connection.cursor() as cursor_target:
                                cursor_target.execute(call_procedure_column_sql)

                            column_pre = column_now
                            column_id += 1
                        # 排除建表语句中可能没有拆分干净的分表语句等杂项
                        elif all(keyword not in final_sentence for keyword in ['PRIMARY', 'ENGINE=InnoDB', 'PARTITION']):
                            key_name = final_sentence.split("`")[1]
                            key = final_sentence.split("(`")[1].split("`")[0]
                            if "udx" in key_name:
                                call_procedure_column_sql = f"CALL add_element_unless_exists('index', '{table_name}', '{key_name}', 'ALTER TABLE {table_name} ADD UNIQUE INDEX {key_name} ({key}) USING BTREE');\n"
                            else:
                                call_procedure_column_sql = f"CALL add_element_unless_exists('index', '{table_name}', '{key_name}', 'ALTER TABLE {table_name} ADD INDEX {key_name} ({key}) USING BTREE');\n"
                            table_call_messages += call_procedure_column_sql
                            with self.target_connection.cursor() as cursor_target:
                                cursor_target.execute(call_procedure_column_sql)
                    self.log_message(table_call_messages)
        except Exception as e:
            self.log_message(f"生成表{table_name} 插入语句失败: {e}")
            raise e

    def fix_structure_by_file(self, file_path):
        create_tables = []
        current_statement = []
        in_create_table = False
        in_call_lines = False
        call_lines = []
        call_message = ""

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # 处理建表语句部分
            for line in lines:
                # 检查是否进入 CREATE TABLE 语句块
                if line.strip().startswith('CREATE TABLE'):
                    in_create_table = True

                # 如果在CREATE TABLE块中，添加当前行
                if in_create_table:
                    current_statement.append(line)

                # 如果遇到分号并且在 CREATE TABLE 块中，表示语句结束
                if in_create_table and line.strip().endswith(';'):
                    create_tables.append(''.join(current_statement))
                    current_statement = []
                    in_create_table = False

                # 处理 "全量更新所有表字段" 之后的插入语句
                if "全量更新所有表字段" in line:
                    in_call_lines = True

                if in_call_lines:
                    call_lines.append(line.strip())

            # 执行 CREATE TABLE 语句
            cursor = self.target_connection.cursor()
            for table_sql in create_tables:
                try:
                    self.log_message(f"执行补表：{table_sql}")
                    cursor.execute(table_sql)
                except Exception as e:
                    self.log_message(f"执行补表失败: {e}")
                    raise e

            # 执行后续插入或补充字段/索引的语句
            for call_sql in call_lines:
                try:
                    if call_sql.startswith("--"):
                        self.log_message(f"{call_message}")
                        call_message = ""   # --开头表示一个新表的语句，清空call_message，重新拼接
                        call_message += f"{call_sql}\n"
                    else:
                        call_message += f"{call_sql}\n"
                        if call_sql:    # 过滤空白行
                            cursor.execute(call_sql)
                except Exception as e:
                    self.log_message(f"执行补字段/索引插入失败: {e}")
                    raise e    # 打的是最后一次的部分
            self.target_connection.commit()

        except Exception as e:
            self.log_message(f"执行补表失败: {e}")
            raise e
        finally:
            self.log_message(f"成功执行字段/索引插入：{call_message}")


class MainWindow(tk.Tk):
    """UI界面类"""

    def __init__(self):
        super().__init__()

        # 页面组件
        self.start_button = None
        self.log_text = None
        self.base_db_select = None
        self.base_database_input = None
        self.password_input = None
        self.user_input = None
        self.port_input = None
        self.host_input = None

        # 基线库配置信息
        self.base_host = "101.91.144.186"
        self.base_port = 13049
        self.base_user = "findcar_read"  # 云端基线库账号，全表只读账号
        self.base_password = "Keytop@2024"

        self.title(f"数据库结构补全工具-{version}")
        self.geometry("800x600")
        # self.resizable(False, False)

        self.create_widgets()
        self.center_window(800, 600)

        # 线程安全的日志队列
        self.log_queue = queue.Queue()
        self.after(100, self.process_log_queue)

        self.parking_guidance_databases = []  # 缓存parking_guidance_x.x.x数据库名，后续切换的时候展示用
        self.fetch_parking_guidance_databases()  # 初始化时查询并缓存数据

        # 处理 PyInstaller 打包后的路径
        if getattr(sys, 'frozen', False):
            # PyInstaller打包后的路径（sys._MEIPASS是临时目录）
            self.base_path = sys._MEIPASS
        else:
            # 开发环境下的路径
            self.base_path = os.path.dirname(__file__)

        # ktpark_fix.sql的路径
        self.ktpark_path = os.path.join(self.base_path, "ktpark_fix.sql")
        self.parking_guidance_323_path = os.path.join(self.base_path, "parking_guidance_3.2.3_fix.sql")

    def fetch_parking_guidance_databases(self):
        """从云端基线库获取所有符合'parking_guidance_x.x.x'格式的数据库名并缓存"""
        connection = None
        try:
            connection = pymysql.connect(
                host=self.base_host,
                user=self.base_user,
                password=self.base_password,
                port=self.base_port,
                connect_timeout=10,
                read_timeout=10
            )

            with connection.cursor() as cursor:
                # 查询所有符合'parking_guidance_x.x.x'格式的数据库名
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name REGEXP '^parking_guidance_[0-9]+\\.[0-9]+\\.[0-9]+$';
                """)
                databases = cursor.fetchall()

                # 提取表名并更新下拉列表
                database_names = [database[0] for database in databases]

                # 定义一个函数来提取版本号，并将其转换为元组(major, minor, patch)
                def parse_version(name):
                    """从数据库名中提取版本号并转换为(major, minor, patch)格式的元组，方便后续处理"""
                    version_numbers = re.findall(r'\d+', name)
                    return tuple(map(int, version_numbers)) if version_numbers else (0, 0, 0)

                # 过滤掉小于3.2.3的版本号
                filtered_databases = []
                for db_name in database_names:
                    version = parse_version(db_name)
                    if version >= (3, 2, 3):
                        filtered_databases.append((db_name, version))

                # 按版本号进行排序
                sorted_databases = sorted(filtered_databases, key=lambda x: x[1])

                # 提取排序后的数据库名
                sorted_database_names = [db[0] for db in sorted_databases]

                self.parking_guidance_databases = sorted_database_names

        except Exception as e:
            messagebox.showwarning("提示", f"连接到基线库失败，正在使用【离线模式】\n右侧基准结构库只能选择内置的基础版本")
        finally:
            if connection:
                connection.close()

    def create_widgets(self):
        # 主框架，使用 grid 布局管理
        self.grid_rowconfigure(0, weight=2)  # 上半部分占五分之二
        self.grid_rowconfigure(1, weight=3)  # 下半部分占五分之三
        self.grid_columnconfigure(0, weight=1)  # 列权重为 1，保证填满整个窗口

        # 上半部分（左右分区）
        top_frame = tk.Frame(self, padx=20, pady=20)
        top_frame.grid(row=0, column=0, sticky="nsew")

        # 下半部分（日志框和按钮）
        bottom_frame = tk.Frame(self, padx=20, pady=20)
        bottom_frame.grid(row=1, column=0, sticky="nsew")

        # 左右框架
        left_frame = tk.Frame(top_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_frame = tk.Frame(top_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 左侧表单布局
        tk.Label(left_frame, text="待修复的数据库信息:").grid(row=0, column=0, pady=5, sticky=tk.W)

        tk.Label(left_frame, text="\t数据库IP:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.host_input = tk.Entry(left_frame)
        self.host_input.insert(0, "127.0.0.1")
        self.host_input.grid(row=1, column=1, pady=5, sticky=tk.W + tk.E)

        tk.Label(left_frame, text="\t数据库端口:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.port_input = tk.Entry(left_frame)
        self.port_input.insert(0, "5831")
        self.port_input.grid(row=2, column=1, pady=5, sticky=tk.W + tk.E)

        tk.Label(left_frame, text="\t用户名:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.user_input = tk.Entry(left_frame)
        self.user_input.insert(0, "root")
        self.user_input.grid(row=3, column=1, pady=5, sticky=tk.W + tk.E)

        tk.Label(left_frame, text="\t密码:").grid(row=4, column=0, pady=5, sticky=tk.W)
        self.password_input = tk.Entry(left_frame, show="*")
        self.password_input.insert(0, "Keytop:wabjtam!")
        self.password_input.grid(row=4, column=1, pady=5, sticky=tk.W + tk.E)

        tk.Label(left_frame, text="\t数据库名称:").grid(row=5, column=0, pady=5, sticky=tk.W)
        self.base_database_input = ttk.Combobox(left_frame, values=["ktpark", "parking_guidance"])
        self.base_database_input.grid(row=5, column=1, pady=5, sticky=tk.W + tk.E)
        # 绑定事件到左侧下拉框
        self.base_database_input.bind("<<ComboboxSelected>>", self.update_base_db_select)

        # 右侧布局（选择基准库）
        tk.Label(right_frame, text="想要以哪个版本结构来修复当前库:").grid(row=1, column=0, pady=5, sticky=tk.W)

        tk.Label(right_frame, text="\t选择云端基准结构库:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.base_db_select = ttk.Combobox(right_frame, values=["请先选择左侧现场数据库名称"])
        self.base_db_select.grid(row=2, column=1, pady=5, sticky=tk.W + tk.E)

        # 下部分（日志框和按钮）
        # 滚动条
        log_scrollbar = tk.Scrollbar(bottom_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 日志显示框
        self.log_text = tk.Text(bottom_frame, state=tk.DISABLED, height=15, yscrollcommand=log_scrollbar.set)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 关联滚动条和文本框
        log_scrollbar.config(command=self.log_text.yview)

        # 按钮
        self.start_button = tk.Button(bottom_frame, text="开始结构修复", command=self.start_completion_in_thread)
        self.start_button.pack()

    def center_window(self, window_width, window_height):
        """使窗口居中显示"""
        # 获取屏幕宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 计算窗口的居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def update_base_db_select(self, event):
        """根据左侧下拉框的选择动态更新右侧下拉框的选项"""
        selected_option = self.base_database_input.get()

        if selected_option == "ktpark":
            if self.parking_guidance_databases:
                # 如果左侧选择ktpark，右侧下拉框只显示ktpark
                self.base_db_select['values'] = ["ktpark"]
            else:
                self.base_db_select['values'] = ["内置_ktpark"]
            self.base_db_select.set(self.base_db_select['values'][0])  # 设置默认选中项
        elif selected_option == "parking_guidance":
            # 如果左侧选择parking_guidance，右侧下拉框显示缓存的parking_guidance相关数据库
            if self.parking_guidance_databases:
                self.base_db_select['values'] = self.parking_guidance_databases
            else:
                self.base_db_select['values'] = ["内置_parking_guidance_3.2.3"]
            self.base_db_select.set(self.base_db_select['values'][0])  # 设置默认选中项

        else:
            # 清空右侧下拉框
            self.base_db_select['values'] = []
            self.base_db_select.set("")

    def log(self, message):
        """将日志消息放入队列"""
        self.log_queue.put(f"{datetime.now()} - {message}")

    def process_log_queue(self):
        """从队列中获取日志并更新到日志框"""
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.config(state=tk.DISABLED)
            self.log_text.see(tk.END)
        self.after(100, self.process_log_queue)

    def start_completion_in_thread(self):
        """在新线程中执行修复操作，否则太耗时会阻塞主UI无响应"""
        threading.Thread(target=self.start_completion, daemon=True).start()

    def start_completion(self):
        """执行修复操作"""
        # 先检查是否选择了数据库
        if not self.base_database_input.get() or not self.base_db_select.get():
            messagebox.showwarning("警告", "请先选择数据库")
            return

        # 先弹宇宙免责声明
        proceed = messagebox.askokcancel(
            "友情提示",
            "结构修复理论上不会造成原数据被破坏~\n但是出于安全考虑，开始修复前最好还是自行做个数据备份~\n\n“确定”开始修复，“取消”停止操作"
        )

        if not proceed:
            self.log("用户取消了修复操作")
            return  # 用户选择取消时，停止操作

        self.log("========开始数据库结构修复========")
        self.start_button.config(state=tk.DISABLED)
        # 获取输入的目标库数据
        target_host = self.host_input.get()
        target_port = int(self.port_input.get())
        target_user = self.user_input.get()
        target_password = self.password_input.get()
        target_database = self.base_database_input.get()

        # 基线库信息
        base_database = self.base_db_select.get()
        # 初始化
        app = Application(
            self.base_host, self.base_port, self.base_user, self.base_password, base_database,
            target_host, target_port, target_user, target_password, target_database,
            self.log
        )

        if "内置" in base_database:
            self.log(f"选择使用{base_database}修复，开始读取内置sql并执行")
            if base_database == "内置_ktpark":
                file_path = self.ktpark_path
            elif base_database == "内置_parking_guidance_3.2.3":
                file_path = self.parking_guidance_323_path
            else:
                self.log(f"无法识别的内置库名：{base_database}，已停止修复！")
                self.start_button.config(state=tk.NORMAL)
                return
            # 开始执行
            try:
                app.connect_to_target_database()    # 初始化目标数据库连接
                app.insert_procedure_sentences()    # 插入存储过程

                app.fix_structure_by_file(file_path)
                app.init_config_tables()  # 检查四张配置表，没有值的话新增默认数据
                self.log("数据库结构修复成功完成！")
            except Exception as e:
                self.log(f"执行时发生错误: {e}\n\n结构补全失败，已停止进程！！！")
                return
            finally:
                # 完成后关闭数据库连接
                app.disconnect_dbs()
                self.start_button.config(state=tk.NORMAL)
        # 如果能连基线库，从基线库动态生成
        else:
            try:
                app.connect_to_target_database()  # 初始化目标数据库连接
                app.connect_to_base_database()  # 初始化源数据库连接

                # 从基线库动态构建语句并执行到待修复数据库
                app.insert_procedure_sentences()
                app.get_all_construct_sentences()
                app.init_config_tables()    # 检查四张配置表，没有值的话新增默认数据
                # ktpark和parking_guidance分别走各自的逻辑
                if "ktpark" in target_database:
                    app.get_all_column_insert_sentences_ktpark()
                elif "parking_guidance" in target_database:
                    app.get_all_column_insert_sentences_parking_guidance()

                self.log("数据库结构修复成功完成！")
            except Exception as e:
                self.log(f"执行时发生错误: {e}\n\n结构补全失败，已停止进程！！！")
                return
            finally:
                # 完成后关闭数据库连接
                app.disconnect_dbs()
                self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
