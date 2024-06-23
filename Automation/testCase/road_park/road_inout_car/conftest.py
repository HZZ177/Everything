# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: conftest.py
@Description: 用例前置/后置
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/02
===================================
"""
import importlib
import traceback

import allure
import pytest

from common.configLog import logger
from common.filepath import config
from service.road_park.api.tollManService import TollManService
from service.hardware_platform import hardWarePlatformAuthService
from service.hardware_platform.hardwardPlatManageService import HardWarePlatformManageService
from service.road_park.manage import roadTollSystemService
from service.road_park.manage.formCenter.carDetailService import CarDetailService
from service.road_park.manage.formCenter.feeDetailService import FeeDetailService
from service.road_park.manage.park_manage.basicInfoService import BasicInfoService
from service.road_park.manage.park_manage.ruleConfigService import RuleConfigService
from service.road_park.manage.park_manage.tollmanManageService import TollManManageService
from testCase.road_park.road_inout_car import parking_info, no_Free_stopTime, fix_car_info, inout_car_info, free_stopTime, \
    free_time

manage_token = ""
hard_ware_platform_token = ""
metaclass = None


@pytest.fixture()
def setupAndTeardown(request, globalSessionSetupAndTeardown, init_fixture, z_removeAllCars, no_owe, getPath):
    """
    前后置操作
    :param 前后自带参数
    :param globalSessionSetupAndTeardown: 全局session fixture
    :param init_fixture: 模块级别初始化fixture
    :param no_owe: 自定义数据处理fixture
    :param z_removeAllCars: 自定义数据处理fixture
    :param getPath 用例自带前后置
    :param init_fix_car_case_session 用例自带前初始化
    :return:
    """
    logger.info("=================================【【正在进行前置处理】】=================================")
    try:
        # 全局session级别前置数据
        global_session_dic = globalSessionSetupAndTeardown
        # 获得用例级别conftest文件模块
        global metaclass
        import_name = getPath
        # logger.info(f"当前 import_name【{import_name}】")
        metaclass = importlib.import_module(import_name)
        # 方法前置级别的数据
        set_up_dic = setup()
        logger.info(f"当前管理平台token【{manage_token}】")
        test_data_dict = {"parking_info": parking_info, "inout_car_info": inout_car_info, "free_time": free_time,
                          "no_Free_stopTime": no_Free_stopTime, "free_stopTime": free_stopTime,
                          "fix_car_info": fix_car_info}
        test_data_dict.update(set_up_dic)
        yield test_data_dict
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc(), f"错误信息为：{msg}"))
    finally:
        pass
    teardown()
    logger.info("=================================【【正在进行后置处理】】=================================")


def setup():
    """
    前置处理函数
    :return:
    """
    try:
        start_dict = metaclass.start_operation()
        return start_dict if start_dict else {}
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc()))


def teardown():
    """
    后置处理函数
    :return:
    """
    try:
        end_dict = metaclass.end_operation()
    except Exception as msg:
        raise Exception(logger.error(traceback.format_exc()))


@pytest.fixture(scope="session")
@allure.step("登录管理系统")
def road_roll_system_session_setup():
    # 储存收费系统管理端token
    road_toll_system_token = roadTollSystemService.RoadTollSystemService().login_manage()
    global manage_token
    manage_token = road_toll_system_token["token"]
    return {"road_toll_system_token": road_toll_system_token["token"]}


@pytest.fixture(scope="session")
@allure.step("登录硬件云平台")
def road_hard_ware_platform_session_setup(road_roll_system_session_setup):
    # 储存收费系统管理端token
    road_hard_ware_platform_token = hardWarePlatformAuthService.HardWarePlatformAuthService().login_hard_ward_platform()
    global hard_ware_platform_token
    hard_ware_platform_token = road_hard_ware_platform_token["token"]
    return {"road_hard_ware_platform_token": road_hard_ware_platform_token["token"]}


@pytest.fixture(scope='session')
@allure.title('初始化：创建路段')
def init_add_road(road_hard_ware_platform_session_setup):
    try:
        # 添加路段
        roadName = '自动化测试路段'
        BasicInfoService().road_add(roadName)
        road_info = BasicInfoService().get_road_info(roadName=roadName)['data']['records'][0]
        road_id, parking_info['roadCode'] = road_info['id'], road_info['roadCode']
    except:
        raise Exception('添加路段失败')
    yield
    # 删除路段
    BasicInfoService().road_disable(road_id=road_id)


@pytest.fixture(scope='session')
@allure.title('初始化：新增收费员')
def init_add_tollman(init_add_road):
    tollmanName = 'dwb007'
    try:
        # 新增收费员
        TollManManageService().add_toll_man(tollmanName, tollmanName)
        tollman_info = TollManManageService().get_toll_man_list(username=tollmanName)['data']['records'][0]
        parking_info['tollmanId'], parking_info['tollmanName'] = tollman_info['id'], tollmanName
    except:
        raise Exception('新增收费员失败')
    yield
    # 删除收费员
    TollManManageService().disable_toll_man(tollman_info['id'])


@pytest.fixture(scope='session')
@allure.title('初始化：新增工作站')
def init_add_workstation(init_add_tollman):
    workstationName = '自动化测试工作站'
    try:
        # 创建工作站
        TollManManageService().add_workstation(workstationName)
        workstation_info = TollManManageService().get_workstation_list(workstationName=workstationName)['data']['records'][0]
        parking_info['workstationName'], parking_info['workstationId'] = workstationName, workstation_info['id']
    except:
        raise Exception('添加工作站失败')
    yield
    # 删除工作站
    TollManManageService().disable_workstation(workstation_info['id'])


@pytest.fixture(scope='session')
@allure.title('初始化：创建车位，工作站绑定车位和收费员')
def init_bind_parkspace_and_tollman(init_add_workstation):
    roadCode, workstationName = parking_info['roadCode'], parking_info['workstationName']
    try:
        parking_info['parkSpaceCode1'], parking_info['parkSpaceCode2'] = "1", "2"
        # 创建车位
        parkspace_code1, parkspace_code2 = parking_info['parkSpaceCode1'], parking_info['parkSpaceCode2']
        BasicInfoService().park_space_add(parkspace_code1, roadCode)
        BasicInfoService().park_space_add(parkspace_code2, roadCode)
        parkspaces_info = BasicInfoService().get_park_space_info(roadCode=roadCode)['data']['records']
        ids = [parkspace['id'] for parkspace in parkspaces_info]
        # 工作站绑定车位和收费员
        tollmanId, workstationId = parking_info['tollmanId'], parking_info['workstationId']
        TollManManageService().update_workstation(workstationId, tollmanId, ids,
                                                  workstationName=parking_info['workstationName'])
    except:
        raise Exception('创建车位失败')


@pytest.fixture(scope='session')
@allure.title('初始化：添加计费规则并绑定路段')
def init_add_fee_rule(init_bind_parkspace_and_tollman):
    roadCode = parking_info['roadCode']
    # 新建计费规则
    ruleName = '自动化测试计费规则'
    result = RuleConfigService().add_rule_group(ruleName, ruleName, periodCapFeeYuan='0.01', freeTimeMin=5)
    if result.get('msg') == '车场下已存在相同名称计费规则':
        RuleConfigService().delete_rule_group(ruleName)
        RuleConfigService().add_rule_group(ruleName, ruleName, periodCapFeeYuan='0.01', freeTimeMin=5)
    fee_id = RuleConfigService().get_fee_id(ruleName)
    try:
        RuleConfigService().fee_batch_bind(ruleName, roadCode)
    except Exception:
        RuleConfigService().delete_rule_group(fee_id=fee_id)
        raise Exception('计费规则绑定路段失败')
    yield
    # 删除计费规则
    RuleConfigService().delete_rule_group(fee_id=fee_id)


@pytest.fixture(scope='session')
@allure.title('初始化：手持机登录->选择工作站')
def init_app_login(init_add_fee_rule):
    try:
        # 登录
        payload = {'username': parking_info['tollmanName'], 'password': parking_info['tollmanName']}
        TollManService().login(**payload)
        # 选择工作站
        tollmanId = parking_info['tollmanId']
        workstationId = parking_info['workstationId']
        TollManService().select_workstation(tollmanId, workstationId)
    except Exception:
        raise Exception('手持机登录失败')


@pytest.fixture(scope='session')
def init_fixture(init_app_login):
    # 获取parkId
    parkId = BasicInfoService().parking_page()['data']['records'][0]['id']
    parking_info['parkId'] = parkId


@pytest.fixture()
@allure.title('每条用例跑看，检查路段没有欠费')
def no_owe():
    yield
    FeeDetailService().clean_allOwe_inRoad(**parking_info)
    # roadCode = parking_info['roadCode']
    # escapeRecords = feeDetail_serve.escape_page(roadCode=roadCode)['data']['records']
    # if len(escapeRecords) == 0:
    #     return
    # else:
    #     time.sleep(0.5)
    # assert False, '有欠费'


@pytest.fixture
@allure.title('车位绑定地磁')
def add_parkSpace_bindIot():
    roadCode, parkId, berth = parking_info['roadCode'], parking_info['parkId'], parking_info['parkSpaceCode2']
    road_name = BasicInfoService().get_road_info(roadCode=roadCode)['data']['records'][0]['roadName']
    # 车位绑定地磁
    deviceCode = config.get("hardware_platform").get("iot_imei")
    HardWarePlatformManageService().bind(parkId, roadCode, berth, deviceCode, roadName=road_name)
    yield berth
    # 地磁解绑车位
    HardWarePlatformManageService().unbind(parkId, berth, roadCode)


@pytest.fixture()
@allure.title('车位绑定高位相机')
def add_parkSpace_bindCamera():
    parkId, roadCode, parkspaceCode = parking_info['parkId'], parking_info['roadCode'], parking_info['parkSpaceCode2']
    road_name = BasicInfoService().get_road_info(roadCode=roadCode)['data']['records'][0]['roadName']
    # 车位绑定高位相机
    deviceCode = config.get("hardware_platform").get('cameraId')
    HardWarePlatformManageService().bind(parkId, roadCode, parkspaceCode, deviceCode, '2', roadName=road_name)
    yield parkspaceCode
    # 高位相机解绑车位
    HardWarePlatformManageService().unbind(parkspaceCode=parkspaceCode, **parking_info)


@pytest.fixture()
@allure.title('车位绑定低位视频桩')
def add_parkSpace_bindLowVideo():
    parkspaceCode = parking_info['parkSpaceCode2']
    parkId, roadCode = parking_info['parkId'], parking_info['roadCode']
    road_name = BasicInfoService().get_road_info(roadCode=roadCode)['data']['records'][0]['roadName']
    # 车位绑定低位视频桩
    deviceCode = config.get("hardware_platform").get('low_video_deviceId')
    HardWarePlatformManageService().bind(parkId, roadCode, parkspaceCode, deviceCode, '3', roadName=road_name)
    yield parkspaceCode
    # 低位视频桩解绑车位
    HardWarePlatformManageService().unbind(parkspaceCode=parkspaceCode, **parking_info)


@allure.step('清除所有在场车')
@pytest.fixture(scope='function')
def z_removeAllCars():
    yield
    # records = CarDetailService().present_car_page(**parking_info)['data']['records']
    records = CarDetailService().present_car_page()['data']['records']
    while records:
        for record in records:
            CarDetailService().out_car(**record)
        records = CarDetailService().present_car_page()['data']['records']