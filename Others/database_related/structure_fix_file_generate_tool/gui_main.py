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
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'w', encoding="utf-8") as file:
                    for table in tables:
                        table_name = table[0]
                        file.write(f"Table: {table_name}\n")

                        cursor.execute(f"DESCRIBE {table_name}")
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
CREATE PROCEDURE add_element_unless_exists(IN element_type VARCHAR(64), IN tab_name VARCHAR(64), IN element_name VARCHAR(64), IN sql_statement VARCHAR(500))
BEGIN
    IF element_type = 'column' THEN
        IF NOT EXISTS (SELECT * FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = tab_name AND column_name = element_name) THEN
            SET @s = sql_statement;
            PREPARE stmt FROM @s;
            EXECUTE stmt;
        END IF;
    END IF;

    IF element_type = 'index' THEN
        IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.STATISTICS WHERE table_schema = DATABASE() AND table_name = tab_name AND index_name = element_name) THEN
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
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量创建标准库表===============\n")
                    for table in tables:
                        table_name = table[0]
                        file.write(f"-- 构造表 {table_name}\n")

                        cursor.execute(f"show create TABLE {table_name}")
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
                cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
                tables = cursor.fetchall()

                with open(self.output_file, 'a', encoding="utf-8") as file:
                    file.write("-- ===============全量更新所有表字段===============\n")
                    for table in tables:
                        table_name = table[0]
                        file.write(f"-- 更新表 {table_name} 所有字段和索引\n")

                        cursor.execute(f"""SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA
                                            FROM INFORMATION_SCHEMA.COLUMNS
                                            WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}';""")
                        columns = cursor.fetchall()

                        cursor.execute(f"""SELECT INDEX_NAME, NON_UNIQUE, INDEX_TYPE, COLUMN_NAME
                                            FROM INFORMATION_SCHEMA.STATISTICS
                                            WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}';""")
                        indexes = cursor.fetchall()

                        column_id = 0
                        column_pre = None

                        for column in columns:
                            column_name, column_type, is_nullable, column_default, column_key, extra = column
                            nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                            default = f"DEFAULT {column_default}" if column_default else ""
                            extra_info = extra if extra else ""

                            column_definition = f"{column_name} {column_type} {nullable} {default} {extra_info}".strip()
                            escaped_definition = column_definition.replace("'", "\\'")

                            if column_id == 0:
                                file.write(
                                    f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition};');\n"
                                )
                            else:
                                file.write(
                                    f"CALL add_element_unless_exists('column', '{table_name}', '{column_name}', 'ALTER TABLE {table_name} ADD COLUMN {escaped_definition} AFTER {column_pre};');\n"
                                )
                            column_pre = column_name
                            column_id += 1

                        for index in indexes:
                            index_name, non_unique, index_type, column_name = index
                            index_type = "UNIQUE" if non_unique == 0 else "INDEX"
                            index_statement = f"ADD {index_type} INDEX {index_name} ({column_name}) USING BTREE"
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
        self.host_input = QLineEdit(self)
        self.port_input = QLineEdit(self)
        self.user_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.database_input = QLineEdit(self)

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

        base_database = self.base_db_select.currentText()
        output_file = f"{base_database}_sql_completion.sql"

        app = Application(host, port, user, password, database, output_file)
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
