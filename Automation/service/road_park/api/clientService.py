# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: clientService.py
@Description: 路侧C端相关服务
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/07/06
===================================
"""
import time

import allure
import faker

from common import filepath, util
from common.configLog import logger
from common.filepath import config
from model.road_park.road_client_api import send_road_client_api


class ClientService:
    """
    C端相关的接口

    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("C端购买固定车卡套餐预下单")
    def preOrder(self, comboId, buyNum=1, cardId=None, carNos=None, cardName=None, phone=None, cardParkspaceNum=10,
                 remark="", parkCode="", **kwargs):
        """
        C端购买固定车卡套餐预下单 - /third/customer/api/fix/preOrder

        @param comboId: 套餐id
        @param buyNum: 购买数量
        @param cardId: 固定车卡id
        @param carNos: 车牌列表
        @param cardName: 固定车卡名
        @param phone: 电话号
        @param cardParkspaceNum: 车位
        @param remark: 备注
        @param parkCode: 车厂编号
        @param args:
        @param kwargs:
        @return:
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
            "parkCode": parkCode,
            "comboId": comboId,
            "buyNum": buyNum,
            "cardId": cardId,
            "carNos": carNos if carNos else [],
            "cardName": cardName if cardName else config.get('fix_card')['cardName'],
            "phone": phone if phone else config.get('fix_card')['phone'],
            "cardParkspaceNum": cardParkspaceNum,
            "remark": remark
        }
        kwargs.update(test_data)
        res = send_road_client_api(filepath.ROAD_CLIENT_FIX_PRE_ORDER, 4, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ C端购买固定车卡【{cardId}】套餐【{comboId}】预下单成功！")
            return result_dic
        else:
            raise Exception(f"❌ C端购买固定车卡【{cardId}】套餐【{comboId}】预下单失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("C端充值支付成功回调")
    def PayOverOrder(self, orderNo, payMoney, stcOrderNo=None, merOrderNo=None, payTime=None, totalMoney=None, freeMoney=0,
                     payChannel=5, payType=1, cOrderNo=None, **kwargs):
        """
        C端充值支付成功回调 - /third/customer/api/fix/paySuccess

        @param orderNo: 预下单订单号
        @param payMoney: 支付金额
        @param stcOrderNo: 速停车订单号
        @param merOrderNo: 商户订单号
        @param payTime: 支付时间
        @param totalMoney: 订单总金额
        @param freeMoney: 优惠金额
        @param payChannel: 支付渠道 0-未知 1-线下车场 2-速停车 3-速停车小票应用 4-联创 5-车主端 默认 5
        @param payType: 支付方式 0-现金 1-微信 2-支付宝 3-银联 4-线上转账 5-优惠券 6-其他 99-聚合一码付 默认1
        @param cOrderNo: C端订单号
        @param kwargs:
        @return:
        """
        fake = faker.Faker()
        test_data = {
                "orderNo": orderNo,
                "payMoney": payMoney,
                "stcOrderNo": stcOrderNo if stcOrderNo else fake.pystr(32, 32).upper(),
                "merOrderNo": merOrderNo if merOrderNo else fake.pystr(27, 27).upper(),
                "cOrderNo": cOrderNo if cOrderNo else fake.pystr(32, 32).upper(),
                "payTime": payTime if payTime else int(time.time() * 1000),
                "totalMoney": totalMoney if totalMoney else payMoney,
                "freeMoney": freeMoney,
                "payChannel": payChannel,
                "payType": payType
            }
        kwargs.update(test_data)
        res = send_road_client_api(filepath.ROAD_CLIENT_FIX_PAY_SUCCESS, 4, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ C端订单【{orderNo}】支付回调成功！")
            return result_dic
        else:
            raise Exception(f"❌ C端订单【{orderNo}】支付回调失败！错误为【{res.text}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过C端充值固定车卡")
    def recharge_fix_card(self, comboId, carNos, *args, **kwargs):
        """
        通过C端充值固定车卡 - /api/app/searchCar

        :param comboId: 套餐号
        :param carNos: 车牌号列表

        """
        order_info = self.preOrder(comboId=comboId, carNos=carNos, *args, **kwargs)["data"]
        orderNo, payMoney = order_info["orderNo"], order_info["payMoney"]
        return self.PayOverOrder(orderNo, payMoney, *args, **kwargs)