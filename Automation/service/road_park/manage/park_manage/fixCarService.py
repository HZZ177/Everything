# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: fixCarService.py
@Description:
车场管理
    固定车管理
        固定车卡管理
        固定车区域划分
        固定车充值套餐
        固定车卡类型
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/26
===================================
"""
import time

import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from common.generate_data import generate_data
from model.road_park.road_toll_system_api import send_road_toll_system_api


class FixCarService:
    """
    固定车管理模块相关serve
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车区域管理——》列表查询（分页）")
    def area_search(self, areaName='', parkCode="", **kwargs):
        """
        固定车区域管理——》列表查询（分页）

        :param areaName: 区域名称
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "areaName": areaName
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_SEARCH_PARKING_AREA, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查找车场【{parkCode}】的固定车区域【{areaName}】的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查找车场【{parkCode}】的固定车区域【{areaName}】的失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车区域管理——》路段信息列表查询(修改按钮)")
    def get_area_road_info(self, parkCode, roadName='', size=1000, current=1, **kwargs):
        """
        固定车区域管理——》路段信息列表查询(修改按钮)

        :param roadName: 路段名称
        :param parkCode: 车场编码
        :param size: 每页显示数量
        :param current: 当前页
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
                'roadName': roadName,
                'parkCode': parkCode,
                'current': current,
                'size': size
            }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_AREA_ROAD_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查找车场【{parkCode}】的固定车区域路段的信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查找车场【{parkCode}】的固定车区域路段的信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车区域管理 -> 新增")
    def area_add(self, areaName, parkCode="", **kwargs):
        """
        固定车区域管理 -> 新增

        :param areaName: 区域名称
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "areaName": areaName
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_AREA, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】增加固定车区域【{areaName}】的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】增加固定车区域【{areaName}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车区域管理 —> 修改")
    def area_modify(self, areaName, bind_road_code=None, un_r_code=None, parkCode="", new_areaName='', **kwargs):
        """
        固定车区域管理 —> 修改

        :param areaName: 区域名称
        :param new_areaName: 修改区域名称
        :param parkCode: 车场编码
        :param bind_road_code: 新增的路段编码
        :param un_r_code: 解绑的路段编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        bind_road_code = [] if bind_road_code is None else bind_road_code
        un_r_code = [] if un_r_code is None else un_r_code
        area_info = self.area_search(areaName)['data']['records'][0]
        area_id = area_info['id']
        areaRoad, add_road, un_road_code = [], [], []
        roads = self.get_area_road_info(parkCode)['data']['records']
        # 原始绑定的路段信息，新增的路段信息，解绑的路段信息
        areaRoad_base = {
            "areaId": area_id,
            "parkCode": parkCode
        }
        bind_roads = [
            {'roadName': i.get('roadName'), 'roadCode': i.get('roadCode'), 'parkspaceNum': i.get('parkspaceNum')} for i
            in roads if i.get('areaId') == area_id]  # 获取已绑定路段的信息

        if isinstance(bind_road_code, str):  # 新增绑定路段的信息
            bind_road_code = [bind_road_code]
        for bind_r_code in bind_road_code:
            bind_r_info = [{'roadName': r_code['roadName'], 'parkspaceNum': r_code['parkspaceNum'],
                            'roadCode': r_code['roadCode']} for r_code in roads if bind_r_code == r_code['roadCode']]
            if bind_r_info:
                add_road.append(bind_r_info[0])
        if isinstance(un_r_code, str):  # 找出解绑路段信息
            un_r_code = [un_r_code]
        for un_r_code in un_r_code:
            un_road_info = [{'roadName': r_code['roadName'], 'parkspaceNum': r_code['parkspaceNum'],
                             'roadCode': r_code['roadCode']} for r_code in roads if un_r_code == r_code['roadCode']]
            if un_road_info:
                un_road_code.append(un_road_info[0])
        # 已绑定的路段、新绑定路段和解绑路段运算逻辑
        areaRoad = bind_roads + add_road
        # unbind_r_code = list(set(areaRoad) & set(un_road_code))
        [areaRoad.remove(i) for i in un_road_code if i in areaRoad]

        [i.update(areaRoad_base) for i in areaRoad]
        areaName = new_areaName if new_areaName else areaName
        test_data = {"id": area_id,
                     "areaName": areaName,
                     "parkCode": parkCode,
                     "areaRoad": areaRoad
                     }
        res = send_road_toll_system_api(filepath.MANAGE_MODIFY_PARKING_AREA, 1, header_data={}, test_data=test_data)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】修改固定车区域【{areaName}】的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】修改固定车区域【{areaName}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车区域管理——》删除")
    def area_delete(self, areaName='', areaId='', parkCode="", **kwargs):
        """
        固定车区域管理——》删除

        :param areaId: 区域ID
        :param areaName: 区名称
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        if not areaId:
            areaId = self.area_search(parkCode, areaName, **kwargs)['data']['records'][0]['id']
        test_data = {"id": areaId,
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DELETE_PARKING_AREA, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】删除固定车区域【{areaId}】的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】删除固定车区域【{areaId}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车卡管理 - 添加固定车卡")
    def add_fix_card(self, carNo, cardName: str, phone: str, parkspaceNum, fixCardTypeId, carType=None, remark='',
                     parkCode="", **kwargs):
        """
        固定车卡管理 - 添加固定车卡

        :param parkCode: 车场编码
        :param cardName: 车主名称
        :param carNo: 车牌号列表
        :param carType: 车辆类型
        :param phone: 电话号码
        :param parkspaceNum: 新增固定车卡中车位数量
        :param fixCardTypeId: 固定车卡类型ID
        :param remark: 备注
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        # 车牌绑定逻辑
        if isinstance(carType, list):
            fixCarNoList = [{'carNo': i[0], 'carType': i[1]} for i in zip(carNo, carType)]
        else:
            if (carType == 0) or carType:
                if isinstance(carNo, str):
                    carNo = [carNo]
                # fixCarNoList = [{'carNo': i, 'carType': carType} for i in carNo]
            else:
                if isinstance(carNo, str):
                    carNo = [carNo]
                carType = generate_data.random_carType()
            fixCarNoList = [{'carNo': i, 'carType': carType} for i in carNo]
        test_data = {'parkCode': parkCode,
                     'cardName': cardName,
                     'phone': phone,
                     'parkspaceNum': parkspaceNum,
                     'fixCardTypeId': fixCardTypeId,
                     'remark': remark,
                     'fixCarNoList': fixCarNoList
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_FIX_CARD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】的新增固定车卡【{cardName}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】的新增固定车卡【{cardName}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("新增固定车卡类型")
    def add_fix_card_type(self, parkCode="", fixCardType="", fixCardTypeDesc='', applyFlag=0, chargeFlag=0, **kwargs):
        """
        新增固定车卡类型

        :param parkCode: 车场编码
        :param fixCardType: 固定车卡类型名称
        :param fixCardTypeDesc: 固定车卡类型描述
        :param applyFlag: 是否允许三方自助申请
        :param chargeFlag: 是否允许三方自助充值
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "fixCardType": fixCardType,
                     "fixCardTypeDesc": fixCardTypeDesc,
                     "applyFlag": applyFlag,
                     "chargeFlag": chargeFlag
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_FIX_CARD_TYPE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】的新增固定车卡类型【{fixCardType}】成功！")
        else:
            raise Exception(f"❌ 车场【{parkCode}】的新增固定车卡类型【{fixCardType}】失败！错误为【{result_dic}】!")
        records = self.page_fix_card_type()['data']['records']
        # 固定车卡类型ID：fixCardTypeId；固定车卡id：type_id；固定车卡类型名称：fixCardType
        car_type_info = [{'fixCardTypeId': i['fixCardTypeId'], 'type_id': i['id']} for i in records if
                         i['fixCardType'] == kwargs['fixCardType']][0]
        result_dic.update(car_type_info)
        return result_dic

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询固定车卡类型")
    def page_fix_card_type(self, parkCode="", size=10, current=1, **kwargs):
        """
        分页查询固定车卡类型

        :param parkCode: 车场编码
        :param current: 当前页
        :param size: 每页显示数量
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "current": current,
                     "size": size,
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_PAGE_PARKING_FIX_CARD_TYPE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查找车场【{parkCode}】的固定车卡类型的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查找车场【{parkCode}】的固定车卡类型的失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("删除固定车卡类型")
    def delete_fix_card_type(self, parkCode="", type_id='', fixCardType='', **kwargs):
        """
        删除固定车卡类型

        :param parkCode: 车场编码
        :param type_id: 固定车卡类型ID
        :param fixCardType: 固定车卡类型名称
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        if not type_id:
            fix_car_type = self.page_fix_card_type(parkCode, size=100)['data']['records']
            type_info = [{'id': i['id'], 'fixCardTypeId': i['fixCardTypeId']} for i in fix_car_type if
                         fixCardType == i['fixCardType']]
            if type_info:
                type_info = type_info[0]
            else:
                logger.info(f"不存在类型为【{fixCardType}】的固定车卡类型，不进行删除操作！！！")
                return
            test_data = {"parkCode": parkCode}
            test_data.update(type_info)
        else:
            test_data = {"parkCode": parkCode,
                         "id": type_id}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DELETE_PARKING_FIX_CARD_TYPE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】删除固定车卡类型【{fixCardType}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】删除固定车卡类型【{fixCardType}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("新增固定车充值套餐")
    def fix_combo_add(self, name, fixCardTypeId, areaIdList, chargeNum, fee=0, parkCode="",
                      startDate='', endDate='', feeByParkspace=False, thirdRecharge=False, **kwargs):
        """
        新增固定车充值套餐

        :param name: 套餐名
        :param fixCardTypeId: 固定车卡类型id
        :param areaIdList: 套餐中的区域
        :param chargeNum: 充值数量
        :param fee: 购买一个套餐的费用
        :param parkCode: 车场编码
        :param startDate: 套餐生效起始时间
        :param endDate: 套餐生效结束时间
        :param feeByParkspace: 是否按车位计费 false:否（默认） true：是
        :param thirdRecharge: 是否允许第三方自助缴费 false:否（默认） true：是
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        # 套餐有效期给个默认
        if not startDate:
            startDate = generate_data.g_today() + ' 00:00:00'
        if not endDate:
            endDate = generate_data.adjust_time(startDate, month=120)
        startDate, endDate = startDate.split()[0], endDate.split()[0]
        if feeByParkspace:
            feeByParkspace = True
        # 区域选择逻辑
        if isinstance(areaIdList, str):
            areaIdList = [areaIdList]
        test_data = {"parkCode": parkCode,
                     "name": name,
                     "fixCardTypeId": fixCardTypeId,
                     "areaIdList": areaIdList,
                     "startDate": startDate,
                     "endDate": endDate,
                     "chargeNum": chargeNum,
                     "fee": fee,
                     "feeByParkspace": feeByParkspace,
                     "thirdRecharge": thirdRecharge,
                     "giveFlag": False
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_FIX_COMBO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】新增固定车充值套餐【{name}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】新增固定车充值套餐【{name}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车充值套餐分页列表")
    def fix_combo_page(self, parkCode="", name='', size=10, current=0, **kwargs):
        """
        固定车充值套餐分页列表

        :param parkCode: 车场编码
        :param name: 套餐名称
        :param size: 每页显示数量
        :param current: 当前页
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
                'name': name,
                'parkCode': parkCode,
                'current': current,
                'size': size
            }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_PAGE_FIX_COMBO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查找车场【{parkCode}】的固定车充值套餐分页列表的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查找车场【{parkCode}】的固定车充值套餐分页列表的失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车卡管理 -> 固定车卡列表查询（分页）")
    def fix_card_search(self, carNo='', cardName='', parkCode="", **kwargs):
        """
        固定车卡管理 -> 固定车卡列表查询（分页）

        :param carNo: 车牌号
        :param cardName: 车卡主名字
        :param parkCode: 车场编码
        """
        if isinstance(carNo, list):
            carNo = carNo[0]
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {'carNo': carNo,
                     'parkCode': parkCode,
                     'cardName': cardName
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_SEARCH_PARKING_FIX_CARD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查找车场【{parkCode}】的固定车卡的成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查找车场【{parkCode}】的固定车卡的失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车卡充值")
    def fix_card_recharge(self, carNo, cardName, name, fixComboNum, payType=0, parkCode="", remark='', **kwargs):
        """
        固定车卡充值

        :param parkCode: 车场编码
        :param carNo: 车牌号
        :param cardName: 车卡主名称
        :param name: 充值套餐名字
        :param fixComboNum: 充值数量
        :param payType: 充值方式  0: 现金 1: 微信 2: 支付宝 3: 银联 4: 线上转账 5: 优惠券 6: 其他 7: ETC 99: 聚合一码付
        :param remark: 充值备注
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        # 充值之前就知道固定车卡的车卡类型
        # 根据车卡类型匹配充值套餐
        fix_card_info = self.fix_card_search(carNo, cardName)['data']['records'][0]
        fix_card_info = {
            'cardId': fix_card_info['id'],
            'fixCardTypeStr': fix_card_info['fixCardTypeStr'],
            # 'fixCardTypeId': fix_card_info['fixCardTypeId'],
            # 'parkspaceNum': fix_card_info['parkspaceNum'],
            # 'phone': fix_card_info['phone']
        }
        # 充值套餐信息
        combo_infos = self.combon_list_by_f_card_type_id(parkCode, **kwargs)['data']
        combo_info = [combo for combo in combo_infos if combo['name'] == name][0]
        if not combo_info:
            raise Exception('没有找到车卡匹配的固定车充值套餐')

        feeByParkspace = 1 if combo_info['feeByParkspace'] else 0
        # 实收金额计算逻辑
        fee = combo_info['fee'] * fixComboNum if feeByParkspace else combo_info['fee']
        combo_pay = {
            'fixComboId': combo_info['id'],
            'feeByParkspace': feeByParkspace,
            'fee': fee,
            'rechargeType': combo_info['chargeType'],
            'rechargeCount': combo_info['chargeNum'] * fixComboNum,  # 实际充值数量
            'giveType': combo_info['giveType'],
            'giveCount': combo_info['giveNum'] * fixComboNum,  # 实际赠送数量
            'remark': remark
        }
        combo_pay.update(fix_card_info)
        test_data = {
                'cardName': cardName,
                'parkCode': parkCode,
                'fixComboName': name,
                'fixComboNum': fixComboNum,
                'feeByParkspace': feeByParkspace,
                'fee': fee,
                'payType': payType,
                'remark': remark
            }
        test_data.update(combo_pay)
        res = send_road_toll_system_api(filepath.MANAGE_RECHARGE_PARKING_FIX_CARD, 1, header_data={}, test_data=test_data)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】的充值固定车卡【{cardName}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】的充值固定车卡【{cardName}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("固定车卡删除")
    def delete_fix_card(self, cardId='', carNo='', cardName='', parkCode="", **kwargs):
        """
        固定车卡删除

        :param parkCode: 车场编码
        :param carNo: 车牌号
        :param cardName: 车卡主名称
        :param cardId: 车卡id
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        if (carNo or cardName) and (not cardId):
            fixCard = self.fix_card_search(carNo, cardName, parkCode,**kwargs)['data']['records']
            if fixCard:
                fixCard = fixCard[0]
                cardId = fixCard['id']
            else:
                logger.info(f"不存在【{cardName}】的固定车卡，不进行删除！！")
                return
        else:
            raise Exception('车牌号车卡主名字必须有一个')
        test_data = {"id": cardId,
                     "parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DELETE_PARKING_FIX_CARD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车场【{parkCode}】删除固定车卡【{cardId}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 车场【{parkCode}】删除固定车卡【{cardId}】失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("获取指定车型的充值套餐列表")
    def combon_list_by_f_card_type_id(self, parkCode="", fixCardTypeId="", **kwargs):
        """
        获取指定车型的充值套餐列表

        :param parkCode: 车场编码
        :param fixCardTypeId: 固定车卡类型ID
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {'parkCode': parkCode,
                     'fixCardTypeId': fixCardTypeId
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_LIST_BY_FIX_CARD_TYPE_ID, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 获得车场【{parkCode}】固定车卡类型为【{fixCardTypeId}】的固定车卡套餐成功！")
            return result_dic
        else:
            raise Exception(f"❌ 获得车场【{parkCode}】固定车卡类型为【{fixCardTypeId}】的固定车卡套餐失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("新增固定车卡的公共方法")
    def public_add_fix_card(self, carNo, parkspaceNum=None, **kwargs):
        """
        新增固定车卡的公共方法，并充值（充3月赠送0，费用为0）

        :param carNo: 车牌号（固定车卡车牌号，充值的车牌号）
        """
        # 新增固定车卡
        payload = config.get('fix_card')
        if parkspaceNum:
            payload.update({"parkspaceNum": parkspaceNum})
        kwargs.update(payload)
        self.add_fix_card(carNo, **kwargs)
        # 充值
        self.fix_card_recharge(carNo, **kwargs)
        time.sleep(0.3)
        return {
            'cardName': payload['cardName']
        }


if __name__ == '__main__':
    # from service.road_park.manage.roadTollSystemService import RoadTollSystemService
    # RoadTollSystemService().login_manage()
    FixCarService().delete_fix_card_type(fixCardType="test")
    # FixCarService().area_search("自动化区域")