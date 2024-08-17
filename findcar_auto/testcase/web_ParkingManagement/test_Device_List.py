#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Device_List.py
# @Software: PyCharm
# @description: 设备列表页面相关功能自动化

import os
import allure
import pytest
from datetime import datetime
from findcar_auto.common import file_path
from findcar_auto.common.file_tool import FileTool
from findcar_auto.common.db_tool import DBTool
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()
db = DBTool()


class TestDeviceList:

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-进入默认查询1页10个设备信息")
    def test_query_floor_info(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"默认查询1页10个设备列表"):
            message = findCar_admin_api.query_deviceinfo(pagenumber=1, pagesize=10, token=config.get('Token'))
        with allure.step(f"判断查询结果"):
            devices_count = len(message['data']['records'])
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"接口带参查询楼层信息成功，当前查询到的设备个数：{devices_count}")

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-设备列表校准")
    def test_align_devices(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口触发设备列表校准"):
            message = findCar_admin_api.align_devices(token=config.get('Token'))
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            logger.info(f"校准设备列表成功，接口返回：{message.get('message')}")

    @allure.story("车场维护-设备列表")
    @allure.title("车场维护-设备列表-导出设备列表并校验")
    @allure.description('导出设备列表，校验导出文件行数是否与数据库设备数一致')
    def test_export_devicelist(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口触发设备列表导出"):
            res = findCar_admin_api.export_deviceList(token=config.get('Token'))
        with allure.step(f"判断导出结果，若成功保存则导出内容为文件"):
            assert res.status_code == 200, f"导出设备列表失败，请检查接口返回信息：{res}"
            # 如果assert通过，尝试保存二进制导出内容为文件
            today = datetime.today().strftime('%Y%m%d')
            export_path = os.path.join(file_path.test_file_path, f'device_list_export_{today}.xlsx')
            try:
                with open(f'{export_path}', 'wb') as file:
                    file.write(res.content)
                logger.info(f'导出设备列表成功，保存文件路径：{export_path}')
            except Exception as e:
                logger.error(f'保存文件失败，报错信息：{e}')
        with allure.step('根据数据库查询判断导出文件行数是否符合实际'):
            sql = 'select * from device_info'
            db_devices_num = len(db.query(sql))     # 数据库查询到的设备个数

            file_tool = FileTool(export_path)
            export_rows = file_tool.count_rows_excel()  # 不需要减表头行，函数自动剔除了
            assert export_rows == db_devices_num, f'导出文件行数与数据库查询到的设备个数不符，数据库查询到的设备个数：{db_devices_num}，导出文件行数：{export_rows}'
            logger.info(f'导出文件行数与数据库查询到的设备个数一致，数据库查询到的设备个数：{db_devices_num}，导出文件行数：{export_rows}')


if __name__ == '__main__':
    pytest.main(['-sv'], ['test_Device_List.py'])
