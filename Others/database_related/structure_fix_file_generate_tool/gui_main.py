import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox


class Application:
    def __init__(self, host, port, user, password, database, output_file):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.output_file = output_file
        self.connection = None

    def connect_to_database(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                connect_timeout=10,
                read_timeout=10
            )
        except Exception as e:
            print(f"数据库连接失败: {e}")

    def get_all_tables_and_columns(self):
        self.connect_to_database()
        try:
            with self.connection.cursor() as cursor:
                # 获取所有表名
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'w', encoding="utf-8") as file:
                    for table in tables:
                        table_name = table[0]
                        file.write(f"Table: {table_name}\n")

                        # 获取表中的所有字段名和字段类型
                        cursor.execute(f"DESCRIBE `{table_name}`")
                        columns = cursor.fetchall()

                        for column in columns:
                            field, type_ = column[:2]
                            file.write(f"  Field: {field}, Type: {type_}\n")

                        file.write("\n")

        except Exception as e:
            print(f"获取表和列信息失败: {e}")

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

                        # 获取所有表的初始化语句
                        cursor.execute(f"show create TABLE `{table_name}`")
                        columns = cursor.fetchall()

                        for column in columns:
                            describe = column[1]
                            file.write(f"CREATE TABLE IF NOT EXISTS{str(describe).replace('CREATE TABLE', '')};\n")

                        file.write("\n")

        except Exception as e:
            print(f"获取表结构信息失败: {e}")

    def get_all_column_insert_sentences(self):
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
                                                TABLE_SCHEMA = '{self.database}'
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
                                                TABLE_SCHEMA = '{self.database}'
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
            print(f"获取表结构信息失败: {e}")

    def execute_sql(self):
        """执行生成的SQL文件"""
        try:
            with open(self.output_file, 'r', encoding="utf-8") as file:
                sql_statements = file.read()

            self.connect_to_database()

            with self.connection.cursor() as cursor:
                for statement in sql_statements.split(';'):
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
            self.connection.commit()
            print("SQL文件执行成功！")
        except Exception as e:
            print(f"执行SQL时发生错误: {e}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("数据库结构补全工具")
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        # 现场数据库信息的输入框及默认值
        self.host_input = QLineEdit(self)
        self.host_input.setText("127.0.0.1")  # 默认值
        self.port_input = QLineEdit(self)
        self.port_input.setText("5831")  # 默认值
        self.user_input = QLineEdit(self)
        self.user_input.setText("root")  # 默认值
        self.password_input = QLineEdit(self)
        self.password_input.setText("Keytop:wabjtam!")  # 默认值
        self.database_input = QLineEdit(self)
        self.database_input.setText("")  # 默认值

        self.form_layout.addRow("现场数据库地址:", self.host_input)
        self.form_layout.addRow("端口:", self.port_input)
        self.form_layout.addRow("用户名:", self.user_input)
        self.form_layout.addRow("密码:", self.password_input)
        self.form_layout.addRow("数据库名称:", self.database_input)

        self.base_db_select = QComboBox(self)
        self.base_db_select.addItems(["ktpark", "ktpark_dev", "ktpark_test"])
        self.form_layout.addRow("选择基准库:", self.base_db_select)

        self.start_button = QPushButton("生成并执行SQL", self)
        self.start_button.clicked.connect(self.start_completion)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.start_button)

        self.output_file_label = QLabel("SQL 文件路径:")
        self.layout.addWidget(self.output_file_label)

    def start_completion(self):
        host = self.host_input.text()
        port = int(self.port_input.text())
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()

        # 基线库信息
        base_host = "127.0.0.1"
        base_port = 13049
        base_user = "root"
        base_password = "Keytop:wabjtam!"
        base_database = self.base_db_select.currentText()
        output_file = f"{base_database}_sql_completion.sql"

        app = Application(base_host, base_port, base_user, base_password, base_database, output_file)
        app.get_all_tables_and_columns()
        app.insert_procedure_sentences()
        app.get_all_construct_sentences()
        app.get_all_column_insert_sentences()

        app.execute_sql()
        print(f"SQL 文件已生成并执行: {output_file}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
