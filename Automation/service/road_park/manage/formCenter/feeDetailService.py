# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: feeDetailService.py
@Description:
报表中心
    收费报表
        临停支付明细
        临停找零明细
        固定车充值明细
        结算明细
        退款明细
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/26
===================================
"""
import time
from time import strftime

import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_toll_system_api import send_road_toll_system_api


class FeeDetailService:
    """
    报表中心之收费报表模块下的
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询管理端支付订单")
    def pay_order_page(self, carNo='', payTime: list = None, payType='', payChannel='', paySource='', status='',
                       parkCode="", **kwargs):
        """
        查询欠费明细列表(分页)

        :param parkCode: 车场编码
        :param payTime: 支付时间
        :param carNo: 车牌
        :param payType: 支付方式 0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他7:ETC99:聚合一码付
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        :param paySource:支付来源
        :param status: 支付状态
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        payTime = (f'{payTime[0]} 00:00:00', f'{payTime[1]} 23:59:59') if payTime else (
            f'{strftime("%Y-%m-%d")} 00:00:00', f'{strftime("%Y-%m-%d")} 23:59:59')
        test_data = {"parkCode": parkCode,
                     "carNo": carNo,
                     "payType": payType,
                     "payChannel": payChannel,
                     "paySource": paySource,
                     "status": status,
                     "payTimeStart": payTime[0],
                     "payTimeEnd": payTime[1]
                     }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PAY_ORDER_PAGE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】支付订单信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】支付订单信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("查询欠费明细列表(分页)")
    def escape_page(self, carNo='', outTime=None, roadCode='', parkspaceCode='', statuss=None, parkCode="", **kwargs):
        """
        查询欠费明细列表(分页)
    
        :param outTime: 出车时间
        :param carNo: 车牌
        :param roadCode: 路段编码
        :param parkspaceCode: 车位
        :param statuss: 是否缴清，默认全部。状态多选集合 0: 未缴清 1:已缴清 2:已清除
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        now = strftime("%Y-%m-%d")
        outTime = (f'{now} 00:00:00', f'{now} 23:59:59') if not outTime else (
            f'{outTime[0]} 00:00:00', f'{outTime[1]} 23:59:59')
        statuss = statuss if statuss else [0, 1, 2]
        test_data = {"statuss": statuss,
                     "parkCode": parkCode,
                     "carNo": carNo,
                     "parkspaceCode": parkspaceCode,
                     "outTimeStart": outTime[0],
                     "outTimeEnd": outTime[1],
                     "roadCode": roadCode}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_ESCAPE_PAGE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】欠费明细列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】欠费明细列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("查询固定车充值明细")
    def fixRechargeRecordSearch(self, payTime=None, orderNo=None, cardName="", carNo="", parkCode="", **kwargs):
        """
        查询固定车充值明细

        :param payTime: 充值时间
                example: ["2021-12-28", "2021-12-28"]
        :param orderNo: 订单号
        :param cardName: 车主姓名
        :param carNo: 车牌
        :param parkCode: 车场code
        :return:
        """
        payTimeStart = ""
        payTimeEnd = ""
        parkCode = parkCode if parkCode else config.get("parkCode")
        if payTime is not None:
            payTimeStart = f"{payTime[0]} 00:00:00"
            payTimeEnd = f"{payTime[1]} 23:59:59"
        test_data = {
            "payTimeStart": payTimeStart,
            "payTimeEnd": payTimeEnd,
            "payTime": payTime,
            "orderNo": orderNo,
            "cardName": cardName,
            "carNo": carNo,
            "parkCode": parkCode,
            "current": 1,
            "size": 10
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_SEARCH_PARKING_FIX_RECHARGE_RECORD, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】的固定车卡充值明细列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】的固定车卡充值明细列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("清除欠费")
    def clean_escape(self, cleanMoney, parkingRecordId, nick_id="", nickname="", remark="",  parkCode="", cleanTime="", **kwargs):
        """
        清除欠费

        :param parkCode: 车场编码
        :param cleanMoney: 车场编码
        :param remark: 备注
        :param parkingRecordId: 停车记录id
        :param cleanTime: 清除时间
        :param nickname: 操作员名称
        :param nick_id: 操作员id
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        remark = f'清除金额{cleanMoney}' if not remark else remark
        cleanTime = strftime('%Y-%m-%d %H:%M:%S') if not cleanTime else cleanTime
        test_data = {"remark": remark,
                     "cleanMoney": cleanMoney,
                     "cleanTime": cleanTime,
                     "operatorId": nick_id,
                     "operatorName": nickname,
                     "parkCode": parkCode,
                     "parkingRecordId": parkingRecordId}
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_CLEAN_ESCAPE, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】欠费明细列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场【{parkCode}】欠费明细列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("清除路段下所有欠费")
    def clean_allOwe_inRoad(self, **kwargs):
        escapeRecords = self.escape_page(statuss=[0], **kwargs)['data']['records']
        if not escapeRecords:
            return
        while escapeRecords:
            for record in escapeRecords:
                cleanMoney = record['totalMoney'] - record['payMoney']
                parkingRecordId = record['parkingRecordId']
                self.clean_escape(cleanMoney, parkingRecordId, **kwargs)
            time.sleep(0.5)
            escapeRecords = self.escape_page(statuss=[0], **kwargs)['data']['records']

    @util.catch_exception
    @util.retry_fun
    @allure.step("获取固定车卡充值记录")
    def get_fix_card_recharge_record(self, carNo, cardName=None, payTime=None, *args, **kwargs):
        """
        获取固定车卡充值记录
        @param carNo:
        @param cardName:
        @param payTime:
        @param args:
        @param kwargs:
        """
        payTime = payTime if payTime else [strftime("%Y-%m-%d"), strftime("%Y-%m-%d")]
        count = 0
        while True:
            recharge_record = self.fixRechargeRecordSearch(payTime=payTime, cardName=cardName, carNo=carNo,
                                                                      *args, **kwargs)["data"]['records']
            if recharge_record:
                return recharge_record[0]
            time.sleep(0.7)
            count += 1
            if count == 3:  # 3次（3s）轮询之后，返回fasle
                logger.error(f'❌ 获取获取固定车卡充值记录失败，轮询结束后仍未找到车牌号为【{carNo}】、固定车卡名为【{cardName}】的充值记录！！！')
                return False


if __name__ == '__main__':
    # from service.road_park.manage.roadTollSystemService import RoadTollSystemService
    # RoadTollSystemService().login_manage()
    # 添加路段
    roadName = '自动化测试路段'
    # BasicInfoService().road_add(roadName)
    # road_info = BasicInfoService().get_road_info(roadName=roadName)['data']['records'][0]
    # BasicInfoService().park_space_add(road_info['roadCode'], "1")
    FeeDetailService().escape_page(roadCode="road002289")