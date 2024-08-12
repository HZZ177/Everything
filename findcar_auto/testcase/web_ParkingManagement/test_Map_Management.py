#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/3 下午9:56
# @Author  : Heshouyi
# @File    : test_Map_Management.py
# @Software: PyCharm
# @description:车场地图管理页面相关功能自动化

import allure
import pytest
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger
from findcar_auto.model.findCarApi import findCar_admin_api

config = configger.load_config()


class TestMapManagement:

    @allure.story("车场维护-车场地图管理")
    @allure.title("车场维护-车场地图管理-默认查询ID前10楼层信息")
    def test_query_floor_info(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口查询楼层基础信息"):
            message = findCar_admin_api.query_floorinfo(lotid=1, pagenumber=1, pagesize=10, floorname='', token=config['Token'])
        with allure.step(f"判断查询结果"):
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            floor_on = []
            floor_off = []
            for floor in message['data']['records']:
                if floor['status'] == 1:
                    floor_on.append(f"{floor['floorName']}")
                else:
                    floor_off.append(f"{floor['floorName']}")
            logger.info(f"接口查询楼层基础信息成功，查出楼层数：{message['data']['totalCount']},"
                        f"启用楼层共{len(floor_on)}层：{floor_on},未启用楼层共{len(floor_off)}层：{floor_off}")

    @allure.story("车场维护-车场地图管理")
    @allure.title("车场维护-车场地图管理-带参数查询车场楼层信息")
    def test_query_floor_info_by_id(self):
        logger.info("===========================【正在执行用例】===========================")
        with allure.step(f"接口带参查询楼层信息"):
            wanted_floor_id = 1   # 需要查询的楼层id
            message = findCar_admin_api.query_floorinfo(lotid=1, id=wanted_floor_id, pagenumber=1, pagesize=10, floorname='', token=config['Token'])
        with allure.step(f"判断查询结果"):
            return_floor_id = message['data']['records'][0]['id']
            assert message['message'] == '成功', f"查询失败，请检查接口返回信息：{message}"
            assert return_floor_id == wanted_floor_id, f"查询到的楼层id与期望id不符，请检查"
            logger.info(f"接口带参查询楼层信息成功，目标楼层id：{wanted_floor_id},查询到的楼层id：{return_floor_id}")


if __name__ == '__main__':
    pytest.main(['-sv', 'test_Map_management.py'])
