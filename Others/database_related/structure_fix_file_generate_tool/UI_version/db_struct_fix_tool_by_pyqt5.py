import sys
from datetime import datetime
import pymysql
import subprocess
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox, \
    QDesktopWidget, QSpacerItem, QSizePolicy, QTextEdit


def get_resource_path(relative_path):
    """获取资源文件路径"""
    # 如果程序是打包后的可执行文件，则使用sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


utils_path = get_resource_path("utils")
sql_file = rf"{utils_path}\db_fix_sql.sql"
mysql_path = rf"{utils_path}\mysql.exe"


class Application:
    def __init__(
            self,
            base_host, base_port, base_user, base_password, base_database,
            target_host, target_port, target_user, target_password, target_database,
            output_file,
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

        self.output_file = output_file  # 输出sql修复文件路径
        self.connection = None
        self.log = log  # 日志输出更新函数

    def log_message(self, message):
        """用于输出日志到UI日志控件"""
        if self.log:
            self.log(message)

    def connect_to_base_database(self):
        """连接到基线库"""
        try:
            self.connection = pymysql.connect(
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
            self.connection = pymysql.connect(
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

    def insert_procedure_sentences(self):
        """写入存储过程"""
        self.log_message("开始写入存储过程......")
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
        try:
            with open(self.output_file, 'w', encoding="utf-8") as file:
                file.write(f"SET NAMES utf8mb4;\nSET CHARACTER SET utf8mb4;\n")
                file.write(f"-- ============定义存储过程============\n")
                file.write(f"{procedure_add_element_unless_exists}\n\n")
            self.log_message("存储过程写入成功")
        except Exception as e:
            self.log_message(f"存储过程写入失败: {e}")
            raise e

    def get_all_construct_sentences(self):
        """获取并写入所有表创建语句"""
        self.log_message("开始获取基线表建表语句并写入......")
        self.connect_to_base_database()

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

                        # 获取所有表的初始化语句
                        cursor.execute(f"show create TABLE `{table_name}`")
                        columns = cursor.fetchall()

                        for column in columns:
                            describe = column[1]
                            file.write(f"CREATE TABLE IF NOT EXISTS{str(describe).replace('CREATE TABLE', '')};\n")

                        file.write("\n")

        except Exception as e:
            self.log_message(f"构建并写入建表语句失败: {e}")
            raise e

    def get_all_column_insert_sentences(self):
        """获取并写入所有字段和索引创建语句"""
        self.log_message("开始获取字段和索引创建语句并写入......")
        self.connect_to_base_database()

        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量更新所有表字段===============\n")
                    for table in tables:
                        table_name = table[0]
                        file.write(f"-- 更新表 {table_name} 所有字段和索引\n")

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
                                file.write(
                                    f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition};');\n"
                                )
                            else:
                                file.write(
                                    f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition} AFTER `{column_pre}`;');\n"
                                )
                            column_pre = column_name
                            column_id += 1

                        # 动态生成索引添加语句
                        for index in indexes:
                            index_name, non_unique, index_type, column_name = index
                            index_type = "UNIQUE" if non_unique == 0 else "INDEX"
                            index_statement = f"ADD {index_type} INDEX `{index_name}` (`{column_name}`) USING BTREE"
                            file.write(
                                f"CALL add_element_unless_exists('index', '{table_name}', '{index_name}', 'ALTER TABLE {table_name} {index_statement};');\n"
                            )

                        file.write("\n")

        except Exception as e:
            self.log_message(f"尝试构建并写入字段和索引创建语句失败: {e}")
            raise e

    def execute_sql_file_with_mysql(self):
        """使用mysql客户端工具执行SQL文件"""
        try:
            # 构造mysql执行文件命令
            command = [
                mysql_path,  # mysql客户端的绝对路径
                f"-h{self.target_host}",
                f"-P{self.target_port}",
                f"-u{self.target_user}",
                f"-p{self.target_password}",
                self.target_database
            ]

            # 确保SQL文件存在
            if not os.path.isfile(sql_file):
                self.log_message(f"SQL修复文件{sql_file}不存在")
                raise FileNotFoundError(f"SQL修复文件{sql_file}不存在")

            # 打开SQL文件并通过stdin传递给mysql
            with open(sql_file, "r", encoding="utf-8") as file:
                result = subprocess.run(command, stdin=file, text=True, check=True)
            self.log_message("SQL修复文件执行成功！")

        except subprocess.CalledProcessError as e:
            self.log_message(f"SQL修复文件执行失败，错误代码: {e.returncode}")
            self.log_message(f"错误信息: {e}")
            raise e
        except FileNotFoundError:
            self.log_message(f"请确保MySQL客户端工具{mysql_path}已存在，并在指定路径下")
            raise FileNotFoundError
        except Exception as e:
            self.log_message(f"执行过程中发生错误: {e}")
            raise e


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据库结构补全工具")
        self.setGeometry(100, 100, 800, 600)
        self.center()   # 居中显示主窗口

        # 创建主布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(60, 60, 60, 60)  # 设置布局与窗口的边距

        # 创建表单布局
        self.form_layout = QFormLayout()
        self.form_layout.setVerticalSpacing(20)  # 设置控件垂直间距

        # 初始化各个信息表单
        self.host_input = QLineEdit(self)
        self.host_input.setText("127.0.0.1")

        self.port_input = QLineEdit(self)
        self.port_input.setText("5831")

        self.user_input = QLineEdit(self)
        self.user_input.setText("root")

        self.password_input = QLineEdit(self)
        self.password_input.setText("Keytop:wabjtam!")
        self.password_input.setEchoMode(QLineEdit.Password)  # 隐藏密码

        self.base_database_input = QComboBox(self)
        self.base_database_input.addItems(["ktpark", "parking_guidance3"])  # 默认值

        # 添加表单到界面
        self.form_layout.addRow("现场数据库地址:", self.host_input)
        self.form_layout.addRow("端口:", self.port_input)
        self.form_layout.addRow("用户名:", self.user_input)
        self.form_layout.addRow("密码:", self.password_input)
        self.form_layout.addRow("数据库名称:", self.base_database_input)

        # 基准库选择
        self.base_db_select = QComboBox(self)
        self.base_db_select.addItems(["ktpark", "parking_guidance"])
        self.form_layout.addRow("选择基准库:", self.base_db_select)

        # 添加表单布局到主布局
        self.layout.addLayout(self.form_layout)

        # 添加一个日志显示框（QTextEdit）
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)  # 设置为只读模式
        self.layout.addWidget(self.log_text)

        # 添加一个间隔，用于拉伸控件分布
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 添加执行按钮
        self.start_button = QPushButton("生成并执行SQL", self)
        self.start_button.setFixedHeight(50)  # 设置按钮高度
        self.start_button.setFixedWidth(200)  # 设置按钮宽度
        self.start_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #0078D4;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #003B70;
            }
            """
        )
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_completion)

        # 添加按钮到布局，并使其居中
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.layout.addLayout(button_layout)

    def center(self):
        """使窗口居中"""
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕尺寸
        size = self.geometry()  # 获取窗口尺寸
        # 计算窗口的居中位置
        left = (screen.width() - size.width()) // 2
        top = (screen.height() - size.height()) // 2
        self.move(left, top)

    def log(self, message):
        """将日志信息输出到文本框"""
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.append(f"{time}--{message}")  # 将信息追加到QTextEdit
        QApplication.processEvents()  # 强制更新界面

    def start_completion(self):
        try:
            # 获取界面目标库信息
            target_host = self.host_input.text()
            target_port = int(self.port_input.text())
            target_user = self.user_input.text()
            target_password = self.password_input.text()
            target_database = self.base_database_input.currentText()

            # 基线库信息
            base_host = "127.0.0.1"
            base_port = 5831
            base_user = "root"
            base_password = "Keytop:wabjtam!"
            base_database = self.base_db_select.currentText()

            # 输出文件
            output_file = sql_file

            app = Application(
                base_host, base_port, base_user, base_password, base_database,
                target_host, target_port, target_user, target_password, target_database,
                output_file,
                self.log    # 将log方法传递给Application
            )

            app.insert_procedure_sentences()
            app.get_all_construct_sentences()
            app.get_all_column_insert_sentences()

            app.execute_sql_file_with_mysql()

            self.log(f"数据库结构修复完成")
        except Exception as e:
            self.log(f"执行时发生错误，终止修复!!!\n\n{e}")
            return


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
