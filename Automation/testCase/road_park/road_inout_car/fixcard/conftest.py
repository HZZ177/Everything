"""
@File    : conftest.py
@Time    : 2023/3/17/10:36
@Author  : chenyong
@Software: PyCharm
备注：
"""
import datetime
import random

import allure
import pytest
from common import filepath
from common.configLog import logger
from common.filepath import config
from common.processYaml import Yaml
import platform

from service.road_park.manage.formCenter.carDetailService import CarDetailService
from service.road_park.manage.park_manage.basicInfoService import BasicInfoService
from service.road_park.manage.park_manage.fixCarService import FixCarService
from service.road_park.manage.park_manage.ruleConfigService import RuleConfigService
from service.road_park.manage.park_manage.tollmanManageService import TollManManageService
from testCase.road_park.road_inout_car import fix_car_info, parking_info


@pytest.fixture()
def getPath(init_fix_car_case_session):
    """获取此文件路径"""
    try:
        if 'Windows' == platform.system():
            filenames = __file__.split("\\")
        elif 'Linux' == platform.system():
            filenames = __file__.split("/")
        else:
            raise Exception(f"脚本暂不支持在平台【{platform.system()}】上运行")
        import_name = ".".join(filenames[filenames.index('testCase'):-1] + [filenames[-1][:-3]])
        return import_name
    except Exception as msg:
        raise Exception(logger.error(msg))


def start_operation():
    """
    自定义前置要配置的操作,一定要有此函数，内容根据用例需求配置
    """
    logger.info("=================================【【正在进行用例级别前置处理】】=================================")


def end_operation():
    """
    自定义后置要配置的操作,一定要有此函数，内容根据用例需求配置
    parameter:
    """
    logger.info("=================================【【正在进行用例级别后置处理】】=================================")


@pytest.fixture(scope='session')
@allure.title('添加固定车区域，绑定路段')
def init_add_area():
    areaName, roadCode = 'automator固定车区域', parking_info.get('roadCode')
    if FixCarService().area_add(areaName).get('msg') == '新增成功':
        FixCarService().area_modify(areaName, roadCode)
    else:
        FixCarService().area_delete(areaName)
        FixCarService().area_add(areaName)
    area_id = FixCarService().area_search(areaName)['data']['records'][0]['id']
    fix_car_info['area_id'] = area_id
    yield area_id
    FixCarService().area_delete(areaId=area_id)


@pytest.fixture(scope='session')
@allure.title('初始化：新建固定车卡类型，新增固定车卡充值套餐')
def init_fix_car_type(init_add_area):
    payload = {'fixCardType': 'automator固定车卡类型', 'fixCardTypeDesc': 'automator固定车卡类型描述'}
    with allure.step('初始化：新增固定车卡类型'):
        try:
            car_type_info = FixCarService().add_fix_card_type(**payload)
        except Exception:
            FixCarService().delete_fix_card_type(**payload)
            raise Exception('固定车卡类型创建失败')

    fixCardType_info = {'type_id': car_type_info['type_id'], 'fixCardTypeId': car_type_info['fixCardTypeId']}
    fix_car_info.update(fixCardType_info)
    # 新增固定车充值套餐
    with allure.step('初始化：新增固定车充值套餐'):
        combo_payload = {
            'name': 'automator测试套餐',
            'fixCardTypeId': car_type_info['fixCardTypeId'],
            'areaIdList': fix_car_info['area_id'],
            'chargeNum': 3
        }
        FixCarService().fix_combo_add(**combo_payload)
        fix_car_info.update(combo_payload)
    yield
    FixCarService().delete_fix_card_type(fixCardType=payload['fixCardType'])


@pytest.fixture(scope='session')
@allure.title('初始化：固定车卡session级别的用例fixture')
def init_fix_car_case_session(init_fix_car_type):
    pass
    # global fix_car_info
    # return {"fix_car_info": fix_car_info}


# 以下为固定车卡使用fixture
road_info_list = []
park_space_dict = {}
area_list = []
# 新建计费规则
ruleName_list = ['自动化临停车测试计费规则', '自动化固定车测试计费规则']
# 固定车卡类型
auto_fixCardType = "自动化固定车卡类型"
# 固定车套餐名
auto_fixCardCombo = "自动化测试套餐"


@pytest.fixture(scope='function')
@allure.title('初始化：新增路段自动化1、自动化2、自动化3')
def add_three_road():
    try:
        global road_info_list, park_space_dict
        # 添加路段
        for i in range(1, 4):
            roadName = '自动化测试路段' + f"_{i}"
            BasicInfoService().road_add(roadName)
            road_info = BasicInfoService().get_road_info(roadName=roadName)['data']['records'][0]
            road_id, roadCode = road_info['id'], road_info['roadCode']
            road_info_list.append([road_id, roadCode])
            # 添加车位
            parking_info['parkspaceStartCode'] = 'auto00' + str(random.randint(1, 9))
            num = random.randint(4, 9)
            batch_park_space_info: list = BasicInfoService().add_parking_space_for_road(roadCode, parking_info['parkspaceStartCode'], num)
            parkspaceCode_list = [[_["id"], _["parkspaceCode"]] for _ in batch_park_space_info]
            ids = [_[0] for _ in parkspaceCode_list]
            # 工作站绑定车位和收费员
            tollmanId, workstationId = parking_info['tollmanId'], parking_info['workstationId']
            TollManManageService().update_workstation(workstationId, tollmanId, ids,
                                                      workstationName=parking_info['workstationName'])
            # 记录路段、车位信息
            park_space_dict[roadCode] = [[_["id"], _["parkspaceCode"]] for _ in batch_park_space_info]

    except:
        raise Exception('添加路段失败')
    yield {"road_info": road_info_list, "park_space_dict": park_space_dict}
    # 删除路段
    for road_info in road_info_list:
        if road_info:
            BasicInfoService().road_disable(road_id=road_info[0])
    # 重置路段、车位
    road_info_list = []
    park_space_dict = {}


@pytest.fixture(scope='function')
@allure.title('添加固定车区域，绑定路段')
def add_area(add_three_road):
    global area_list
    areaName = '自动化固定车区域'
    add_three_road_dict = add_three_road
    road_info_list = add_three_road_dict.get("road_info")
    road_code_list = [road_info[1] for road_info in road_info_list]
    if FixCarService().area_add(areaName).get('msg') == '新增成功':
        FixCarService().area_modify(areaName, road_code_list)
    else:
        FixCarService().area_delete(areaName)
        FixCarService().area_add(areaName)
    area_id = FixCarService().area_search(areaName)['data']['records'][0]['id']
    parking_info['area_id'] = area_id
    area_list.append(area_id)
    return_dic = {"area_id": area_list}
    return_dic.update(add_three_road_dict)
    yield return_dic
    # 删除区域
    for area_id in area_list:
        if area_id:
            FixCarService().area_delete(areaId=area_id)
    # 重置区域
    area_list = []


@pytest.fixture(scope='function')
@allure.title('初始化：新建固定车卡类型，新增固定车卡充值套餐')
def new_fix_car_type(add_area):
    add_area_dict = add_area
    payload = {'fixCardType': auto_fixCardType, 'fixCardTypeDesc': f'{auto_fixCardType}描述'}
    with allure.step('初始化：新增固定车卡类型'):
        try:
            car_type_info = FixCarService().add_fix_card_type(**payload)
        except Exception:
            FixCarService().delete_fix_card_type(**payload)
            raise Exception('固定车卡类型创建失败')

    fixCardType_info = {'type_id': car_type_info['type_id'], 'fixCardTypeId': car_type_info['fixCardTypeId']}
    # 新增固定车充值套餐
    with allure.step('初始化：新增固定车充值套餐'):
        combo_payload = {
            'name': auto_fixCardCombo,
            'fixCardTypeId': fixCardType_info['fixCardTypeId'],
            'areaIdList': add_area_dict.get("area_id"),
            'thirdRecharge': True,
            'chargeNum': 3
        }
        FixCarService().fix_combo_add(**combo_payload)
    return_dict = {}
    return_dict.update(fixCardType_info)
    return_dict.update(combo_payload)
    return_dict.update(add_area_dict)
    yield return_dict
    FixCarService().delete_fix_card_type(fixCardType=payload['fixCardType'])


@pytest.fixture(scope='function')
@allure.title('初始化：新增临停、固定计费规则并绑定路段')
def add_fix_tem_fee_rule(new_fix_car_type):
    new_fix_car_type_dict = new_fix_car_type
    road_info_list = new_fix_car_type_dict.get("road_info")
    fix_card_type_id = new_fix_car_type_dict.get("fixCardTypeId")
    for ruleName in ruleName_list:
        periodCapFeeYuan = "0.02" if "临停" in ruleName else '0.01'
        fixFeeType = 0 if "临停" in ruleName else fix_card_type_id
        result = RuleConfigService().add_rule_group(ruleName, ruleName, fixFeeType=fixFeeType, periodCapFeeYuan=periodCapFeeYuan, freeTimeMin=5)
        if result.get('msg') == '车场下已存在相同名称计费规则':
            RuleConfigService().delete_rule_group(ruleName)
            RuleConfigService().add_rule_group(ruleName, ruleName, fixFeeType=fixFeeType, periodCapFeeYuan=periodCapFeeYuan, freeTimeMin=5)
        try:
            RuleConfigService().fee_batch_bind(ruleName, [road_info[1] for road_info in road_info_list])
        except Exception:
            fee_id = RuleConfigService().get_fee_id(ruleName)
            RuleConfigService().delete_rule_group(fee_id=fee_id)
            raise Exception('计费规则绑定路段失败')
    return_dic = {}
    return_dic.update(new_fix_car_type_dict)
    yield return_dic
    # 删除计费规则
    for ruleName in ruleName_list:
        fee_id = RuleConfigService().get_fee_id(ruleName)
        RuleConfigService().delete_rule_group(fee_id=fee_id)


@pytest.fixture(scope='function')
@allure.title('固定车卡前置')
def fix_card_setup(add_fix_tem_fee_rule):
    test_data = add_fix_tem_fee_rule
    return_dict = {"road_info_list": road_info_list, "park_space_dict": park_space_dict,
                   "auto_fixCardCombo": auto_fixCardCombo, "auto_fixCardType": auto_fixCardType}
    return_dict.update(test_data)
    yield return_dict
    with allure.step('清除所有在场车'):
        records = CarDetailService().present_car_page()['data']['records']
        while records:
            for record in records:
                CarDetailService().out_car(**record)
            records = CarDetailService().present_car_page()['data']['records']
    with allure.step('删除固定车卡'):
        try:
            FixCarService().delete_fix_card(cardName=config.get('fix_card')["cardName"])
        except Exception:
            raise Exception("固定车卡删除失败")