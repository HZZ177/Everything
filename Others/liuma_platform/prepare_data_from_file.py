import sys

import openpyxl
import pymysql
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from log_module import logger


def create_db_connection():
    connection = pymysql.connect(
        host='101.227.53.213',
        user='root',
        password='K#2dOho@Dgts',
        database='liuma',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 结果以字典形式返回
    )
    return connection


def get_case_num_by_name(connection, case_name):
    """
    通过用例名称查找平台对应的用例编号，使用现有的数据库连接
    :param connection: 数据库连接对象
    :param case_name: 用例名称
    :return: 用例ID（num），如果找到则返回ID, 否则返回None
    """
    try:
        with connection.cursor() as cursor:
            # SQL 查询语句
            sql = """
            SELECT num FROM `case` 
            WHERE name = %s AND status = 'normal'
            """
            cursor.execute(sql, (case_name,))
            result = cursor.fetchone()
            if result:
                return result['num']
            else:
                logger.error(f"未找到用例名称为【{case_name}】对应的平台用例编号，请注意检查！")
                return None
    except Exception as e:
        logger.error(f"查询用例对应平台编号出现错误: {e}")
        return None


def prepare_data_from_file():
    """
    把Excel文件里的用例编号根据模块整理成dict，通过用例名称查找编号，方便后续脚本更新数据到平台集合中使用
    :return: dict，内部为多个tuple，数据格式：(‘父模块—子模块',[xxx,xxx])
    """
    # 创建一个Tkinter根窗口并隐藏
    Tk().withdraw()

    # 选择用例数据文件
    file_path = askopenfilename(title="请选择用例文件", filetypes=[("Excel files", "*.xlsx *.xls")])

    # 打开Excel文件
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # 判断是否有表头，检查第一行第一列是否为"父模块"，不是直接退出程序
    header = sheet[1]
    if header[0].value != "父模块":
        logger.error("文件的第一行第一列不是'父模块'，请规范文件格式，数据从第二行开始读取，必须有一行表头")
        sys.exit()

    # 创建数据库连接
    connection = create_db_connection()

    # 初始化变量
    result_dict = {}
    current_parent_module = None
    current_sub_module = None

    try:
        # 遍历表格行
        for row in sheet.iter_rows(min_row=2, values_only=True):
            parent_module = row[0]  # 父模块
            sub_module = row[1]     # 子模块
            case_name = row[2]      # 用例名称

            # 如果有父模块，就更新当前父模块
            if parent_module:
                current_parent_module = parent_module

            # 如果有子模块，就更新当前子模块
            if sub_module:
                current_sub_module = sub_module

            # 如果有用例名称，去查找用例编号
            if case_name:
                case_number = get_case_num_by_name(connection, case_name)
                if case_number:
                    # 拼接模块名作为集合名称
                    key = f"{current_parent_module}—{current_sub_module}"
                    if key not in result_dict:
                        result_dict[key] = []
                    result_dict[key].append(case_number)

        # 构建符合要求的格式：将字典的key和value转换为tuple
        result_list = [(key, value) for key, value in result_dict.items()]

    finally:
        # 关闭数据库连接
        connection.close()

    return result_list


if __name__ == "__main__":
    result = prepare_data_from_file()
    print(result)
