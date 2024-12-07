import os
import queue
import re
import sys
import threading
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

        self.base_connection = None     # 基线库连接对象
        self.target_connection = None   # 修复目标库连接对象
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
                cursor.execute(clear_procedure)     # 清除之前存在的存储过程

                self.log_message(f"写入存储过程\n{procedure_add_element_unless_exists}")
                cursor.execute(procedure_add_element_unless_exists)     # 写入存储过程
                self.target_connection.commit()     # 手动提交防止自动提交模式被关闭

            self.log_message("存储过程写入成功！")
        except Exception as e:
            self.log_message(f"存储过程写入失败: {e}")
            raise e

    def get_all_construct_sentences(self):
        """从基线库获取所有表创建语句，动态生成后执行到目标库"""
        self.log_message("开始获取基线库表结构并动态生成......")

        try:    # 从基线库获取所有表名
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

                        self.log_message(crate_sql)     # 打印
                        # 对目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(crate_sql)       # 执行
                        self.target_connection.commit()     # 提交

            self.log_message("动态构建表结构并执行成功！")
        except Exception as e:
            self.log_message(f"构建并执行建表语句失败: {e}")
            raise e

    def get_all_column_insert_sentences(self):
        """获取并写入所有字段和索引创建语句"""
        self.log_message("开始获取字段和索引创建语句并写入......")

        try:        # 在基线库获取
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
                        default = f"DEFAULT {column_default}" if column_default is not None else ""
                        extra_info = extra if extra else ""

                        # 动态生成 SQL 语句
                        column_definition = f"`{column_name}` {column_type} {nullable} {default} {extra_info}".strip()
                        # 转义单引号以支持 SET 类型的字段
                        escaped_definition = column_definition.replace("'", "\\'")

                        if column_id == 0:
                            call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition};');\n"
                        else:
                            call_procedure_column_sql = f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition} AFTER `{column_pre}`;');\n"

                        table_call_messages += call_procedure_column_sql    # 打印
                        # 在目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(call_procedure_column_sql)      # 执行
                        self.target_connection.commit()         # 提交

                        column_pre = column_name
                        column_id += 1

                    # 动态生成索引添加语句
                    for index in indexes:
                        index_name, non_unique, index_type, column_name = index
                        index_type = "UNIQUE" if non_unique == 0 else "INDEX"
                        index_statement = f"ADD {index_type} INDEX `{index_name}` (`{column_name}`) USING BTREE"
                        call_procedure_index_sql = f"CALL add_element_unless_exists('index', '{table_name}', '{index_name}', 'ALTER TABLE {table_name} {index_statement};');\n"

                        table_call_messages += call_procedure_index_sql  # 打印
                        # 在目标库执行
                        with self.target_connection.cursor() as cursor_target:
                            cursor_target.execute(call_procedure_index_sql)    # 执行
                        self.target_connection.commit()             # 提交
                    self.log_message(table_call_messages)
            self.log_message("构建字段和索引创建语句并执行成功！")
        except Exception as e:
            self.log_message(f"构建字段和索引创建语句并执行失败: {e}")
            raise e


class MainWindow(tk.Tk):
    """UI界面类"""
    def __init__(self):
        super().__init__()

        # 基线库配置信息
        self.base_host = "101.91.144.186"
        self.base_port = 13049
        self.base_user = "root"  # 云端基线库账号，root账号方便后续扩展可以用其他库表，程序内只有读操作，不会修改数据
        self.base_password = "Keytop@321"

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
            messagebox.showerror("错误", f"连接基线库加载列表失败: {e}\n请确保网络环境可用")
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
            # 如果左侧选择 ktpark，右侧下拉框只显示 ktpark
            self.base_db_select['values'] = ["ktpark"]
            self.base_db_select.set("ktpark")  # 设置默认选中项
        elif selected_option == "parking_guidance":
            # 如果左侧选择 parking_guidance，右侧下拉框显示缓存的 parking_guidance 数据库
            if self.parking_guidance_databases:
                self.base_db_select['values'] = self.parking_guidance_databases
                self.base_db_select.set(self.parking_guidance_databases[0])  # 设置默认选中项
            else:
                self.base_db_select['values'] = []
                self.base_db_select.set("")
                messagebox.showwarning("警告", "没有找到符合条件的parking_guidance数据库")
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

        try:
            app = Application(
                self.base_host, self.base_port, self.base_user, self.base_password, base_database,
                target_host, target_port, target_user, target_password, target_database,
                self.log
            )

            app.connect_to_target_database()    # 初始化目标数据库连接
            app.connect_to_base_database()      # 初始化源数据库连接

            # 从基线库动态构建语句并执行到待修复数据库
            app.insert_procedure_sentences()
            app.get_all_construct_sentences()
            app.get_all_column_insert_sentences()

            # 完成后关闭数据库连接
            app.disconnect_dbs()
            self.log("数据库结构修复成功完成！")
        except Exception as e:
            self.log(f"执行时发生错误: {e}\n\n结构补全失败，已停止进程！！！")
        finally:
            self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
