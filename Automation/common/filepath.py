# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: filepath.py
@Description: 文件路径管理
@Author: wurun
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
===================================
"""

import os
import time
import yaml

'''项目目录'''
PRO_PATH = os.path.dirname(os.path.realpath(__file__))  # 获取项目目录

'''一级目录'''
TEST_CASE_PATH = os.path.join(PRO_PATH, '../testCase')  # 测试用例存放目录
TEST_DATA_PATH = os.path.join(PRO_PATH, '../testData')  # 测试数据存放目录
TEST_FILE_PATH = os.path.join(PRO_PATH, '../file')  # 测试文件存放目录
LOG_PATH = os.path.join(PRO_PATH, '../logs')  # 日志文件存放目录

'''二级目录'''
ROAD_FILE_PATH = os.path.join(TEST_FILE_PATH, 'road_file')  # 路侧测试文件目录
CONFIG_PATH = os.path.join(TEST_DATA_PATH, 'config')  # 配置参数目录
ROAD_PARK_PATH = os.path.join(TEST_DATA_PATH, 'road_park')  # 路侧收费系统目录
ROAD_HARD_WARD_PLATFORM_PATH = os.path.join(TEST_DATA_PATH, 'road_hardward_platform')  # 硬件云平台管理端目录
ROAD_CLIENT_PATH = os.path.join(TEST_DATA_PATH, 'road_client')  # 路侧C端目录

'''三级目录'''
SETTING_MAP = {
    "local": os.path.join(CONFIG_PATH, 'local_config.yaml'),     # 配置参数，本地
    "test": os.path.join(CONFIG_PATH, 'test_config.yaml'),     # 配置参数，测试
    "prod": os.path.join(CONFIG_PATH, 'prod_config.yaml')     # 配置参数，正式
}
CONFIG_PARAM = os.environ.get("AUTO_CONFIG")
SETTING = SETTING_MAP.get(CONFIG_PARAM) if SETTING_MAP.get(CONFIG_PARAM) else SETTING_MAP.get("local")
TOKEN_FILE = os.path.join(CONFIG_PATH, 'token.json')  # 储存token的json文件
PUBLIC_KEY = os.path.join(ROAD_FILE_PATH, 'pub.txt')  # 公钥文件

# 路侧收费系统
ROAD_PARK_MANAGE = os.path.join(ROAD_PARK_PATH, "manage")  # manage模块
ROAD_PARK_API = os.path.join(ROAD_PARK_PATH, "api")  # api模块
ROAD_PARK_FILE = os.path.join(ROAD_PARK_PATH, "file")  # file模块
ROAD_PARK_THIRD = os.path.join(ROAD_PARK_PATH, "third")  # third模块

# 硬件云管理端
HARD_WARD_PLATFORM_AUTH = os.path.join(ROAD_HARD_WARD_PLATFORM_PATH, "auth")  # 硬件云平台认证相关
HARD_WARD_PLATFORM_MANAGE = os.path.join(ROAD_HARD_WARD_PLATFORM_PATH, "manage")  # 硬件云平台管理相关
HARD_WARD_PLATFORM_NBIOT = os.path.join(ROAD_HARD_WARD_PLATFORM_PATH, "nbiot")  # 硬件云平台出入车相关
HARD_WARD_PLATFORM_VIDEO = os.path.join(ROAD_HARD_WARD_PLATFORM_PATH, "video")  # 硬件云平台相机命令相关
HARD_WARD_PLATFORM_LOW_VIDEO = os.path.join(ROAD_HARD_WARD_PLATFORM_PATH, "low_video")  # 硬件云平台低位视频桩测试命令相关

'''四级目录'''
MANAGE_GET_VERIFICATION_CODE = os.path.join(ROAD_PARK_MANAGE, "authCode.yaml")  # 获得code
MANAGE_AUTH_LOGIN = os.path.join(ROAD_PARK_MANAGE, "authLogin.yaml")  # 登录路侧收费系统管理平台
MANAGE_PARK_REPORT_DAY = os.path.join(ROAD_PARK_MANAGE, "reportGetParkReportDay.yaml")  # 车场运营日报
MANAGE_FUND_CHECK_DAY = os.path.join(ROAD_PARK_MANAGE, "reportFundCheckDay.yaml")  # 资金对账表
MANAGE_TOLL_MAN_PROFIT_DAY = os.path.join(ROAD_PARK_MANAGE, "reportTollmanProfitByDay.yaml")  # 收费员统计
MANAGE_WORK_STATION_DAY_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportWorkStationDayReport.yaml")  # 工作站统计
MANAGE_NIGHT_ESCAPE_ROAD_DAY_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportNightEscapeRoadDayReport.yaml")  # 夜间逃费
MANAGE_LIST_PARK_PROPERTY_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportListParkPropertyReport.yaml")  # 基于车场的固定资产报表
MANAGE_LIST_PARK_PROPERTY_ROAD_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportListParkPropertyRoadReport.yaml")  # 基于路段的固定资产报表
MANAGE_ROAD_DAY_AND_SUM_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportRoadDayAndRoadSum.yaml")  # 路段统计
MANAGE_ROAD_ESCAPE_REPORT = os.path.join(ROAD_PARK_MANAGE, "reportRoadEscapeDayAndRoadSum.yaml")  # 路段逃费明细
MANAGE_TOLL_MAN_EFFICIENCY_DAY = os.path.join(ROAD_PARK_MANAGE, "reportGetTollManEfficiencyDay.yaml")  # 收费员效率分析
MANAGE_PARK_MIN_DETAIL_DAY = os.path.join(ROAD_PARK_MANAGE, "specialreportReportParkMinDetailDay.yaml")  # 停车时长统计
MANAGE_BIG_ORDER_QUERY_DAY_RECORD = os.path.join(ROAD_PARK_MANAGE, "recordParkingSessionBigOrderQueryByDay.yaml")  # 大额逃费
MANAGE_GET_ESCAPE_PAGE = os.path.join(ROAD_PARK_MANAGE, "recordParkingSessionEscapePage.yaml")  # 查询欠费明细列表(分页)  # 分页查询管理端支付订单
MANAGE_CLEAN_ESCAPE = os.path.join(ROAD_PARK_MANAGE, "recordParkingSessionCleanEscape.yaml")  # 清除欠费
MANAGE_LIST_PARKING_SESSION_PAGE = os.path.join(ROAD_PARK_MANAGE, "reportParkingSessionListParkingSessionPage.yaml")  # 分页查询停车计费明细列表
MANAGE_ACCESS_ANALYZE = os.path.join(ROAD_PARK_MANAGE, "analyzeAccessAccessAnalyze.yaml")  # 车流分析
MANAGE_INCOME_ANALYZE = os.path.join(ROAD_PARK_MANAGE, "analyzeIncomeIncomeAnalyze.yaml")  # 收入分析
MANAGE_ADD_PARKING_ROAD = os.path.join(ROAD_PARK_MANAGE, "parkingRoadAdd.yaml")  # 增加车场路段
MANAGE_GET_PARKING_ROAD_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingRoadPage.yaml")  # 分页查询路段
MANAGE_DISABLE_PARKING_ROAD = os.path.join(ROAD_PARK_MANAGE, "parkingRoadDisable.yaml")  # 删除车场路段
MANAGE_ADD_PARKING_TOLL_MAN = os.path.join(ROAD_PARK_MANAGE, "parkingTollManAdd.yaml")  # 添加收费员
MANAGE_GET_PARKING_TOLL_MAN_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingTollManPage.yaml")  # 分页查询收费员列表
MANAGE_DISABLE_PARKING_TOLL_MAN = os.path.join(ROAD_PARK_MANAGE, "parkingTollManDisable.yaml")  # 删除车场收费员
MANAGE_ADD_PARKING_WORKSTATION = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationAdd.yaml")  # 添加工作站
MANAGE_GET_PARKING_WORKSTATION_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationPage.yaml")  # 分页查询工作站列表
MANAGE_DISABLE_PARKING_WORKSTATION = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationDisable.yaml")  # 删除车场工作站
MANAGE_GET_PARKING_WORKSTATION_BOUND_TOLL_MANS = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationBindedTollMansList.yaml")  # 工作站已绑定的收费员列表
MANAGE_GET_PARKING_WORKSTATION_BOUND_PARKING = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationBindedParkingsList.yaml")  # 工作站已绑定的车位列表
MANAGE_UPDATE_PARKING_WORKSTATION = os.path.join(ROAD_PARK_MANAGE, "parkingWorkstationUpdate.yaml")  # 修改工作站
MANAGE_ADD_PARKING_PARK_SPACE = os.path.join(ROAD_PARK_MANAGE, "parkingParkSpaceAdd.yaml")  # 新增单车位
MANAGE_BATCH_ADD_PARKING_PARK_SPACE = os.path.join(ROAD_PARK_MANAGE, "parkingParkSpaceBatchAdd.yaml")  # 批量新增车位
MANAGE_GET_PARKING_PARK_SPACE_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingParkSpacePage.yaml")  # 分页查询车位
MANAGE_GET_PARKING_PARK_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingParkingPage.yaml")  # 查询车场信息
MANAGE_GET_PARKING_PRESENT_CAR_PAGE = os.path.join(ROAD_PARK_MANAGE, "parkingPresentCarPage.yaml")  # 管理端分页查询在场车辆信息
MANAGE_GET_PARKING_EVIDENCE = os.path.join(ROAD_PARK_MANAGE, "parkingParkingEvidence.yaml")  # 管理端查询车辆证据链
MANAGE_OUT_PARKING_PRESENT_CAR = os.path.join(ROAD_PARK_MANAGE, "parkingPresentCarOutCar.yaml")  # 管理端出车
MANAGE_ADD_PARKING_AREA = os.path.join(ROAD_PARK_MANAGE, "parkingAreaAreaAdd.yaml")  # 管理端增加固定车区域
MANAGE_MODIFY_PARKING_AREA = os.path.join(ROAD_PARK_MANAGE, "parkingAreaAreaModify.yaml")  # 管理端修改固定车区域
MANAGE_DELETE_PARKING_AREA = os.path.join(ROAD_PARK_MANAGE, "parkingAreaAreaDelete.yaml")  # 管理端删除固定车区域
MANAGE_SEARCH_PARKING_AREA = os.path.join(ROAD_PARK_MANAGE, "parkingAreaAreaSearch.yaml")  # 管理端列表查询（分页）固定车区域
MANAGE_GET_PARKING_AREA_ROAD_INFO = os.path.join(ROAD_PARK_MANAGE, "parkingAreaGetAreaRoadInfo.yaml")  # 管理端路段信息列表查询(修改按钮)
MANAGE_ADD_PARKING_FIX_CARD_TYPE = os.path.join(ROAD_PARK_MANAGE, "parkingFixCardTypeAdd.yaml")  # 管理端新增固定车卡类型
MANAGE_PAGE_PARKING_FIX_CARD_TYPE = os.path.join(ROAD_PARK_MANAGE, "parkingFixCardTypePageFixCardType.yaml")  # 管理端分页查询固定车卡类型
MANAGE_DELETE_PARKING_FIX_CARD_TYPE = os.path.join(ROAD_PARK_MANAGE, "parkingFixCardTypeDelete.yaml")  # 管理端删除固定车卡类型
MANAGE_ADD_PARKING_FIX_CARD = os.path.join(ROAD_PARK_MANAGE, "parkingNewFixCardAdd.yaml")  # 管理端新增固定车卡
MANAGE_SEARCH_PARKING_FIX_CARD = os.path.join(ROAD_PARK_MANAGE, "parkingFixCardFixCardSearch.yaml")  # 管理端固定车卡列表查询
MANAGE_SEARCH_PARKING_FIX_RECHARGE_RECORD = os.path.join(ROAD_PARK_MANAGE, "parkingFixRechargeRecordFixRechargeRecordSearch.yaml")  # 管理端固定车充值明细查询
MANAGE_RECHARGE_PARKING_FIX_CARD = os.path.join(ROAD_PARK_MANAGE, "parkingNewFixCardFixCardRecharge.yaml")  # 管理端固定车卡充值
MANAGE_DELETE_PARKING_FIX_CARD = os.path.join(ROAD_PARK_MANAGE, "parkingNewFixCardDelete.yaml")  # 管理端删除固定车卡
MANAGE_ADD_FIX_COMBO = os.path.join(ROAD_PARK_MANAGE, "fixComboAdd.yaml")  # 管理端新增固定车卡套餐
MANAGE_LIST_BY_FIX_CARD_TYPE_ID = os.path.join(ROAD_PARK_MANAGE, "fixComboListByFixCardTypeId.yaml")  # 获取指定车型的充值套餐列表
MANAGE_PAGE_FIX_COMBO = os.path.join(ROAD_PARK_MANAGE, "fixComboPage.yaml")  # 固定车充值套餐分页列表
MANAGE_GET_PAY_ORDER_PAGE = os.path.join(ROAD_PARK_MANAGE, "payOrderPage.yaml")
MANAGE_ADD_PARKING_RULE_GROUP = os.path.join(ROAD_PARK_MANAGE, "feeNewAddRuleGroup.yaml")  # 新增计费规则
MANAGE_DEL_PARKING_RULE_GROUP = os.path.join(ROAD_PARK_MANAGE, "feeNewDeleteRuleGroup.yaml")  # 删除计费规则
MANAGE_GET_PARKING_RULE_GROUP_INFO = os.path.join(ROAD_PARK_MANAGE, "feeNewGetRuleGroup.yaml")  # 分页查询计费规则组
MANAGE_BATCH_BIND_PARKING_RULE = os.path.join(ROAD_PARK_MANAGE, "feeNewbatchBind.yaml")  # 批量绑定路段规则
TOLLMAN_LOGIN = os.path.join(ROAD_PARK_API, "tollmanLogin.yaml")  # 收费员登录接口
TOLLMAN_SELECT_WORKSTATION = os.path.join(ROAD_PARK_API, "tollmanSelectWorkstation.yaml")  # 选择工作站接口
APP_PRESENT_DETAIL = os.path.join(ROAD_PARK_API, "appGetPresentDetail.yaml")  # APP在场车详情页
APP_PRESENTS = os.path.join(ROAD_PARK_API, "appGetPresents.yaml")  # APP全部在场车信息
UPLOAD_FILE_BASE64 = os.path.join(ROAD_PARK_FILE, "manageUploadBase64.yaml")  # 上传base64位的图片
APP_REGISTER_IN_CAR = os.path.join(ROAD_PARK_API, "appRegisterInCar.yaml")  # 手持机入车
APP_OUT_CAR = os.path.join(ROAD_PARK_API, "appOut.yaml")  # POS机出车
APP_GET_FEE = os.path.join(ROAD_PARK_API, "appGetFee.yaml")  # 车辆查费
APP_GET_BILL = os.path.join(ROAD_PARK_API, "appGetBill.yaml")  # 查询车辆待缴账单
APP_THIRD_PAY_QUERY = os.path.join(ROAD_PARK_API, "appThirdPayQuery.yaml")  # 第三方支付订单查询
APP_ORDER = os.path.join(ROAD_PARK_API, "appOrder.yaml")  # 车辆下单
APP_OUT_SETTLE = os.path.join(ROAD_PARK_API, "appOutSettle.yaml")  # 结算离场（POS机点击结算离场）
APP_PAY_SUCCESS = os.path.join(ROAD_PARK_API, "appPaySuccess.yaml")  # 现金支付成功（POS机现金支付）
APP_UPDATE_PRESENT_CAR = os.path.join(ROAD_PARK_API, "appUpdatePresentCar.yaml")  # 修改车牌/修改车型
APP_MESSAGE = os.path.join(ROAD_PARK_API, "messagePage.yaml")  # 消息列表

GET_HARD_WARE_CODE = os.path.join(HARD_WARD_PLATFORM_AUTH, "getHardwareVerificationCode.yaml")  # 获得code
LOGIN_HARD_WARD_PLATFORM = os.path.join(HARD_WARD_PLATFORM_AUTH, "loginHardwarePlatform.yaml")  # 登录硬件云管理平台
HARD_WARD_PLATFORM_PARK_SPACE_PAGE = os.path.join(HARD_WARD_PLATFORM_MANAGE, "parkSpacePage.yaml")  # 硬件平台车位绑定页列表查询
HARD_WARD_PLATFORM_PARK_SPACE_BIND = os.path.join(HARD_WARD_PLATFORM_MANAGE, "parkSpaceBind.yaml")  # 硬件平台泊位绑定设备
HARD_WARD_PLATFORM_PARK_SPACE_UNBIND = os.path.join(HARD_WARD_PLATFORM_MANAGE, "parkSpaceUnbind.yaml")  # 硬件平台泊位解绑设备
HARD_WARD_PLATFORM_ONE_NET_CALL_BACK = os.path.join(HARD_WARD_PLATFORM_NBIOT, "oneNetCallBack.yaml")  # 硬件平台移动运营商 - 地磁入车，出车，心跳，其它...
HARD_WARD_PLATFORM_VIDEO_CMD_TEST = os.path.join(HARD_WARD_PLATFORM_VIDEO, "cmdTest.yaml")  # 科拓相机标准入出车测试
HARD_WARD_PLATFORM_LOW_VIDEO_CMD_TEST = os.path.join(HARD_WARD_PLATFORM_LOW_VIDEO, "cmdTest.yaml")  # 低位视频桩测试


ROAD_CLIENT_FIX_PRE_ORDER = os.path.join(ROAD_PARK_THIRD, "customerApiPreOrder.yaml")  # C端购买固定车卡套餐预下单
ROAD_CLIENT_FIX_PAY_SUCCESS = os.path.join(ROAD_PARK_THIRD, "customerApiFixPaySucsess.yaml")  # C端充值支付成功回调


def fetch_path(dir_path):
    """
       生成目录路径
       * @ param path: 目录路径
       * @ return 若目录不存在，则生成
    """
    path = os.path.join(PRO_PATH, dir_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def fetch_path_with_d(dir_path, suffix):
    """
       生成文件路径
       * @ param dir_path: 路径
       * @ param suffix: 文件名后缀
       * @ return 路径+当前日期+当前时间+后缀
    """
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%H_%M_%S', time.localtime(time.time()))
    file_path = os.path.join(fetch_path(dir_path), day)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path, now + suffix)
    return file_name


def del_file(path):
    """
        删除文件
        * @ param path: 需要清除文件夹的路径
    """
    for i in os.listdir(path):
        path_file = os.path.join(path, i)  # 取文件绝对路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


with open(SETTING, 'r', encoding='utf-8') as f:
    file_data = f.read()
config = yaml.load(file_data, Loader=yaml.FullLoader)

if __name__ == '__main__':
    pass
    # print(CONF_PATH.split("\\")[-1])
    # print(XML_REPORT_PATH)
    # del_file(os.path.join(PRO_PATH, '.coverage'))
