# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_fixcar.py
@Description: 固定车卡相关测试用例
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/04
===================================
"""
from time import strftime

import allure

from common.configLog import logger
from common.generate_data import generate_data
from service.road_park.api.appService import AppService
from service.road_park.manage.formCenter.carDetailService import CarDetailService
from service.road_park.manage.park_manage.fixCarService import FixCarService


@allure.epic('固定车卡相关测试用例')
@allure.feature('固定车卡')
@allure.story('固定车卡测试')
class TestFixcar:

    @allure.title('POS机登记入车，临停车改为固定车-web端出车')
    def test_tmpCar_to_fixedCar(self, setupAndTeardown):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("POS机登记入车，临停车改为固定车-web端出车")
        test_data = setupAndTeardown
        parking_info = test_data["parking_info"].copy()
        fix_car_info = test_data["fix_car_info"].copy()
        inout_car_info = test_data["inout_car_info"].copy()
        now, berth = strftime('%Y-%m-%d %H:%M:%S'), parking_info['parkSpaceCode1']
        no_Free_stopTime = test_data["no_Free_stopTime"]
        temp_car, fix_car = generate_data.car_no(1), generate_data.car_no()
        roadCode = parking_info['roadCode']
        with allure.step(f'添加固定车卡，车牌：{fix_car}'):
            FixCarService().public_add_fix_card(fix_car, carType=0, **fix_car_info)
        with allure.step(f'POS机入车-临停车：{temp_car}'):
            inTime = generate_data.adjust_time(now, -no_Free_stopTime)
            temp = AppService().public_in_car(carNo=temp_car, parkspaceCode=berth,  inTime=inTime, carType=3, **inout_car_info, **parking_info)
            # 查看入车消息
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['carNo'] == temp_car, '判断入车失败，理论值：入车车牌'
            assert msg['source'] == 0, '判断入车方式错误，理论值：POS机入车'

        with allure.step('web端【在场车辆明细】页面查看车辆类型'):
            temp_car_info = CarDetailService().present_car_page(carNo=temp_car)['data']['records'][0]
            evidence_info = CarDetailService().evidence(temp['parkingRecordId'])['data']
            assert temp_car_info['carType'] == evidence_info['carType'] == 3, '判断车辆类型错误，理论值：新能源车'
        with allure.step(f'修改临停车：{temp_car}为固定车：{fix_car}，查看详情页显示【固】字'):
            AppService().update_present_car(fix_car, 0, berth, **parking_info)  # 修改在场临停车车牌为固定车车牌
            result = AppService().judge_fixed_or_temp_car(temp['parkingRecordId'], fix_car_info['fixCardTypeId'], parking_info)
            # fix_flag = app_service.get_present_detail(temp['parkingRecordId'], **parking_info)
            assert result, '判断固定车标志错误，理论值：固定车'
        with allure.step('web端【在场车辆明细】页面查看车辆类型'):
            fix_car_detail = CarDetailService().present_car_page(carNo=fix_car)['data']['records'][0]
            assert fix_car_detail['carType'] == 0, '判断车辆类型错误，理论值：小型车'

        with allure.step('返回app首页查看车位卡片上的【固】字'):
            car_info = AppService().get_presents(**parking_info)['data']['roadPresentCars'][0]['presentCars'][0]
            assert car_info['fixFlag'] == fix_car_info['fixCardTypeId'], '判断固定车标志错误，理论值：固定车'
        with allure.step('web端出车'):
            CarDetailService().out_car(fix_car, roadCode, parkspaceCode=berth)
        # 查看出车消息
        msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
        assert msg['carNo'] == fix_car, '判断入车失败，理论值：修改后的车牌'
        assert msg['source'] == 101, '判断入车方式错误，理论值：路内收费系统后台'
        with allure.step('删除固定车卡'):
            try:
                FixCarService().delete_fix_card(carNo=fix_car)
            except Exception:
                raise Exception("固定车卡删除失败")