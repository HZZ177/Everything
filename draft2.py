import pymysql
import calendar

# 数据库连接信息
db_info = {
    "host": "61.171.117.80",
    "port": 12883,
    "user": "stc_parking@test#yongcepro_test",
    "password": "Keytop@Yongce@123",
    "database": "yongcepro",
    "charset": "utf8mb4",  # 确保字符集正确
    "cursorclass": pymysql.cursors.DictCursor  # 以字典形式返回结果
}


def add_day_coefficient_by_month(project_id, year, month):

    # 验证月份
    if not (1 <= month <= 12):
        raise ValueError("月份必须在1到12之间。")

    # 计算当月的天数
    _, num_days = calendar.monthrange(year, month)

    # 生成所有日期
    date_list = [f"{year}-{month:02d}-{day:02d}" for day in range(1, num_days + 1)]

    # 准备要插入的数据
    records = [
        (
            '92b9cc14ba134fc4a0fe74cbf4ef5af2',  # group_id
            project_id,  # project_id
            stat_day,  # stat_day
            3  # day_coefficient
        )
        for stat_day in date_list
    ]

    # 如果DUPLICATE KEY重复插入，则更新
    insert_sql = """
        INSERT INTO t_bs_bd_day_coefficient 
        (`group_id`, `project_id`, `stat_day`, `day_coefficient`) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        day_coefficient = VALUES(day_coefficient)
    """

    try:
        # 连接到数据库
        connection = pymysql.connect(**db_info)

        with connection:
            with connection.cursor() as cursor:
                # 执行批量插入
                cursor.executemany(insert_sql, records)

            # 提交事务
            connection.commit()

        print(f"成功插入/更新 {num_days} 条记录")

    except pymysql.MySQLError as e:
        print("数据库错误：", e)
    except Exception as e:
        print("其他错误：", e)


if __name__ == '__main__':

    project_id = '6000556'
    year = 2025
    month = 1

    add_day_coefficient_by_month(project_id, year, month)
