#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/28 10:35
# @Author  : Heshouyi
# @File    : findcar_report_service.py
# @Software: PyCharm
# @description:

from ..connection.db_connection import DBConnection
from ..utils.file_path import db_path
from ..utils.logger import logger


class FindcarReportService:

    def __init__(self):
        self.db_path = db_path  # 数据库文件路径

    def store_received_message(self, command_data):
        """
        将接收到的上报信息写入数据库
        :param command_data: 接收的寻车上行数据
        :return: None
        """
        # 分辨数据来源，单车场还是统一平台
        if command_data.get("appCode"):     # 有appCode说明来自统一平台
            source = 1
        elif command_data.get("appId"):     # 有appId说明来自单车场
            source = 2
        else:   # 无appCode和appId标记未知
            source = 3
        message_type = command_data.get("cmd")  # 单车场接口应该都有，可能为空，获取不到就存None
        # 存库要求强制str
        command_data = str(command_data).replace("'", '"')

        try:
            # 在使用时创建数据库连接，提前创建会有跨线程问题
            db = DBConnection(self.db_path)  # 初始化数据库连接
            with db:
                insert_sql = "INSERT INTO upper_report_record (source, message_type, message) VALUES (?, ?, ?)"
                db.execute(insert_sql, (source, message_type, command_data))
            logger.info("接收到的寻车上报数据入库成功")
        except Exception as e:
            raise e

    def get_db_history_report(self, page_no, page_size):
        """
        从数据库中获取寻车上报记录
        :return:
        """
        # 计算分页偏移量
        offset = (page_no - 1) * page_size
        sql = f"""
                    SELECT * FROM upper_report_record
                    ORDER BY create_time DESC
                    LIMIT {page_size} OFFSET {offset}
                """
        try:
            db = DBConnection(self.db_path)
            with db:
                return db.fetchall_as_dict(sql)
        except Exception as e:
            raise e
