import pymysql


def delete_database_structure():
    # 连接数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Keytop:wabjtam!',
        database='pg_new',
        port=5831
    )
    cursor = connection.cursor()

    # 获取所有表名
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # 修改每个表
    for table in tables:
        table_name = table[0]

        # 获取所有字段信息
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = cursor.fetchall()

        # 过滤出需要保留的字段（如 id）
        columns_to_keep = [col[0] for col in columns if 'id' in col[0].lower()]

        # 如果没有找到 id 字段，保留第一个字段，避免删除所有字段
        if not columns_to_keep and columns:
            columns_to_keep.append(columns[0][0])

        # 删除需要删除的字段
        for column in columns:
            column_name = column[0]
            if column_name not in columns_to_keep:
                try:
                    cursor.execute(f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`")
                except pymysql.err.OperationalError as e:
                    print(f"删除字段 {column_name} 时发生错误: {e}")

        # 获取所有索引信息
        cursor.execute(f"SHOW INDEX FROM `{table_name}`")
        indexes = cursor.fetchall()

        # 删除所有非主键索引
        for index in indexes:
            index_name = index[2]  # 索引名在第三列
            if index_name != 'PRIMARY':  # 保留主键索引
                try:
                    cursor.execute(f"ALTER TABLE `{table_name}` DROP INDEX `{index_name}`")
                except pymysql.err.OperationalError as e:
                    print(f"删除索引 {index_name} 时发生错误: {e}")

        print(f'表 {table_name} 除主键外的所有字段和索引清除完成')

    # 提交事务
    connection.commit()

    # 关闭连接
    cursor.close()
    connection.close()


if __name__ == '__main__':
    delete_database_structure()
