# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: test_fixcar_supplement.py
@Description: 固定车卡用例补充
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/05
===================================
"""
import random
from time import strftime

import allure

from common.configLog import logger
from common.filepath import config
from common.generate_data import generate_data
from service.road_park.api.appService import AppService
from service.road_park.api.clientService import ClientService
from service.road_park.manage.formCenter.feeDetailService import FeeDetailService
from service.road_park.manage.park_manage.fixCarService import FixCarService


@allure.epic('固定车卡相关测试用例')
@allure.feature('固定车卡')
@allure.story('固定车卡测试')
class TestFixCar:
    """
    固定车卡补充场景相关的测试用例

    """

    @allure.title('删除固定车卡后，车辆计费')
    def test_del_fix_card(self, setupAndTeardown, fix_card_setup):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("删除固定车卡后，车辆计费")
        set_up_test_data = setupAndTeardown
        parking_info = set_up_test_data["parking_info"].copy()
        inout_car_info = set_up_test_data["inout_car_info"].copy()
        no_Free_stopTime = set_up_test_data["no_Free_stopTime"]
        test_data = fix_card_setup
        road_info_list = test_data["road_info_list"].copy()
        park_space_dict = test_data["park_space_dict"].copy()
        # 获得路段信息
        road_info = random.choice(road_info_list)
        roadCode = road_info[1]
        # 获得车位信息
        park_space_info = random.choice(park_space_dict[roadCode])
        now = strftime('%Y-%m-%d %H:%M:%S')
        berth = park_space_info[1]
        # 获得车辆信息
        fix_car = generate_data.car_no()
        fix_card_type_id = test_data.get("fixCardTypeId")
        with allure.step(f'添加固定车卡，车牌：{fix_car}'):
            FixCarService().public_add_fix_card(carNo=fix_car, carType=0, **test_data)
        with allure.step(f'POS机入车：{fix_car}'):
            inTime = generate_data.adjust_time(now, -no_Free_stopTime)
            parking_info.update({"roadCode": roadCode})
            fix = AppService().public_in_car(carNo=fix_car, parkspaceCode=berth, inTime=inTime, carType=0, **inout_car_info, **parking_info)
            # 查看入车消息
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['carNo'] == fix_car, f'判断入车失败，理论值：【{fix_car}】，实际值【{msg["carNo"]}】'
            assert msg['source'] == 0, '判断入车方式错误，理论值：POS机入车'
        with allure.step("查看app端车位显示和收费"):
            record_id = fix["parkingRecordId"]
            app_info = AppService().get_present_detail(record_id, **parking_info)
            assert fix_card_type_id == app_info.get("fixFlag"), f"入场后，app车位显示校验失败，理论值为【{fix_card_type_id}】" \
                                                                f"，实际值为【{app_info.get('fixFlag')}】"
            assert app_info.get("totalFee") == 1, f"入场后，计费规则校验失败，理论值为【1】，实际值为【{app_info.get('totalFee')}】"
        with allure.step("删除固定车卡"):
            FixCarService().delete_fix_card(cardName=config.get('fix_card')["cardName"])
        # with allure.step("查看app端车位停车类型"):
        #     result = AppService().judge_fixed_or_temp_car(record_id, 0, parking_info)
        #     assert result, '判断固定车标志错误，理论值：临停车'
        with allure.step("校验收费"):
            app_info = AppService().get_present_detail(record_id, **parking_info)
            assert app_info.get("totalFee") == 2, f"入场后，计费规则校验失败，理论值为【2】，实际值为【{app_info.get('totalFee')}】"

    @allure.title('C端充值后变为固定车卡（已在场）')
    def test_client_recharge(self, setupAndTeardown, fix_card_setup):
        logger.info("=================================【【正在执行用例】】=================================")
        logger.info("C端充值后变为固定车卡（已在场）")
        set_up_test_data = setupAndTeardown
        parking_info = set_up_test_data["parking_info"].copy()
        inout_car_info = set_up_test_data["inout_car_info"].copy()
        no_Free_stopTime = set_up_test_data["no_Free_stopTime"]
        test_data = fix_card_setup
        road_info_list = test_data["road_info_list"].copy()
        park_space_dict = test_data["park_space_dict"].copy()
        auto_fixCardCombo = test_data["auto_fixCardCombo"]
        # 获得路段信息
        road_info = random.choice(road_info_list)
        roadCode = road_info[1]
        # 获得车位信息
        park_space_info = random.choice(park_space_dict[roadCode])
        now = strftime('%Y-%m-%d %H:%M:%S')
        berth = park_space_info[1]
        # 获得车辆信息
        fix_car = generate_data.car_no()
        fix_card_type_id = test_data.get("fixCardTypeId")
        with allure.step(f'POS机入车：{fix_car}'):
            inTime = generate_data.adjust_time(now, -no_Free_stopTime)
            parking_info.update({"roadCode": roadCode})
            fix = AppService().public_in_car(carNo=fix_car, parkspaceCode=berth, inTime=inTime, carType=0, **inout_car_info, **parking_info)
            # 查看入车消息
            msg = AppService().message(parking_info['workstationId'])['data']['records'][0]
            assert msg['carNo'] == fix_car, f'判断入车失败，理论值：【{fix_car}】，实际值【{msg["carNo"]}】'
            assert msg['source'] == 0, '判断入车方式错误，理论值：POS机入车'
        with allure.step("C端购买套餐A"):
            card_name = config.get('fix_card')['cardName']
            combo_id = FixCarService().fix_combo_page(name=auto_fixCardCombo)['data']['records'][0]["id"]
            ClientService().recharge_fix_card(combo_id, [fix_car], cardName=card_name)
        with allure.step("管理端校验支付来源和渠道"):
            recharge_record = FeeDetailService().get_fix_card_recharge_record(carNo=fix_car, cardName=card_name)
            assert recharge_record, "未获取到充值记录！！"
            assert recharge_record["paySource"] == 5, f"支付来源校验失败！！预期【5】，实际【{recharge_record['paySource']}】"
            assert recharge_record["payChannel"] == 5, f"支付来源校验失败！！预期【5】，实际【{recharge_record['payChannel']}】"
        with allure.step("查看app端车位停车类型"):
            record_id = fix["parkingRecordId"]
            result = AppService().judge_fixed_or_temp_car(record_id, fix_card_type_id, parking_info)
            assert result, '判断固定车标志错误，理论值：固定车'
