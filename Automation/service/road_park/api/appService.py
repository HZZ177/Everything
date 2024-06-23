# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: appService.py
@Description:
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright:
@time:2023/06/30
===================================
"""
import time

import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from common.generate_data import generate_data
from common.mock_third_pay import mock_third_pay
from model.road_park.road_app_api import send_road_app_api
from service.road_park.api.fileService import FileService
from service.road_park.manage.formCenter.carDetailService import CarDetailService


class AppService:
    """
    路内停车助手App车辆相关的接口
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过路内app查询在场车记录")
    def get_present_detail(self, parkingRecordId, tollmanId, **kwargs):
        """通过路内app查询在场车记录

        :param tollmanId: 收费员id
        :param parkingRecordId: 停车记录id
        """
        test_data = {"parkingRecordId": parkingRecordId,
                     "tollmanId": tollmanId}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_PRESENT_DETAIL, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 收费员【{tollmanId}】通过路内app查询在场车记录成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌  收费员【{tollmanId}】通过路内app查询在场车记录失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过路内app查询工作站下全部在场车信息")
    def get_presents(self, parkCode="", tollmanId="", workstationId="", showEmptySpace=1, stopTimeSort=0, **kwargs):
        """查询工作站下全部在场车信息

        :param parkCode: 车场编码
        :param tollmanId: 收费员ID
        :param workstationId: 工作站ID
        :param showEmptySpace: 是否展示空车位 0:不展示 1:展示（默认）
        :param stopTimeSort: 是否按停车时长排序 0:否（默认） 1:按停车时长从短到长排序 2:按停车时长从长到短排序
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode,
                     "tollmanId": tollmanId,
                     "workstationId": workstationId,
                     "showEmptySpace": showEmptySpace,
                     "stopTimeSort": stopTimeSort}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_PRESENTS, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询工作站【{workstationId}】下全部在场车信息成功！")
            return result_dic
        else:
            raise Exception(f"❌  查询工作站【{workstationId}】下全部在场车信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过路内app进行车辆查费")
    def get_fee(self, carNo, parkCode="", **kwargs):
        """通过路内app进行车辆查费

        :param carNo: 车牌号码
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"carNo": carNo,
                     "parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_GET_FEE, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车辆【{carNo}】在车场【{parkCode}】中的费用成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌查询车辆【{carNo}】在车场【{parkCode}】中的费用失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过路内app进行消息列表查询")
    def message(self, workStationId, **kwargs):
        """通过路内app进行消息列表查询

        :param workStationId: 工作站id
        """
        test_data = {"workStationId": workStationId}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_MESSAGE, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询路内app工作站【{workStationId}】的消息列表成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询路内app工作站【{workStationId}】的消息列表失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("下单")
    def order(self, carNo, details: list, parkingRecordIds, settlementType, settlementWay, payChannel, payType,
              parkCode="", parkingRecordId='', **kwargs):
        """
        下单

        :param parkCode: 车场编码
        :param carNo: 车牌号
        :param details: 支付订单明细(必填)
        :param parkingRecordId: 本次停车的停车记录id
        :param parkingRecordIds: 结算停车记录id列表,英文,分割(当该支付后需要结算时必填)
        :param settlementType: 结算类型 0:离场结算（不是在场车的结算） 1:在场结算
        :param settlementWay: 结算方式,0不使用预支付结算,1使用预支付金额结算
        :param payType: 支付方式 0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他7:ETC99:聚合一码付
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        present = CarDetailService().present_car_page(carNo=carNo)['data']['records']
        record_id = present[0]['parkingRecordId'] if present else ''
        test_data = {"carNo": carNo,
                     "details": details,
                     "parkCode": parkCode,
                     "parkingRecordId": record_id,
                     "parkingRecordIds": parkingRecordIds,
                     "payChannel": payChannel,
                     "payType": payType,
                     "settlementType": settlementType,
                     "settlementWay": settlementWay}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_ORDER, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车辆【{carNo}】在车场【{parkCode}】中的下单成功！")
            return result_dic
        else:
            raise Exception(f"❌车辆【{carNo}】在车场【{parkCode}】中的下单失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("查询车辆待缴账单")
    def get_bill(self, carNo, parkCode="", parkingRecordId="", **kwargs):
        """

        :param parkCode: 车场编码
        :param carNo: 车牌号
        :param parkingRecordId: 停车记录ID
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"carNo": carNo,
                     "parkCode": parkCode,
                     "parkingRecordId": parkingRecordId
                     }
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_GET_BILL, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车辆【{carNo}】在车场【{parkCode}】的待缴订单成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车辆【{carNo}】在车场【{parkCode}】的待缴订单失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("第三方支付订单查询")
    def third_pay_query(self, orderNo, parkCode="", payChannel=1, payType=99, **kwargs):
        """

        :param orderNo: 订单号
        :param parkCode: 车场编码
        :param payType: 支付方式，0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他99:聚合一码付
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"orderNo": orderNo,
                     "parkCode": parkCode,
                     "payChannel": payChannel,
                     "payType": payType
                     }
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_THIRD_PAY_QUERY, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询第三方支付订单【{orderNo}】信息成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询第三方支付订单【{orderNo}】信息失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("手持机入车")
    def register_in_car(self, parkCode="", carImg: list = None, **kwargs):
        """
        :param parkCode: 车场编码
        :param carImg: 入车图片

        """
        img_url = []
        parkCode = parkCode if parkCode else config.get("parkCode")
        if carImg:
            if isinstance(carImg, str):
                img_url.append(carImg)
            elif isinstance(carImg, list):
                img_url.extend(carImg)
            carImg = img_url
        else:
            carImg = [FileService().uploadBase64(parkCode=parkCode, **kwargs).get('data')]  # 上传图片，获取pics url
        test_data = {"parkCode": parkCode,
                     "carImg": carImg}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_REGISTER_IN_CAR, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车辆【{kwargs.get('carNo')}】通过手持机入车成功！")
            return result_dic
        else:
            raise Exception(f"❌  车辆【{kwargs.get('carNo')}】通过手持机入车失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS机直接离场（POS机点击直接离场）")
    def out(self, parkCode="", **kwargs):
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_OUT_CAR, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车辆【{kwargs.get('carNo')}】通过pos机出车成功！")
            return result_dic["data"]
        else:
            raise Exception(f"❌  车辆【{kwargs.get('carNo')}】通过pos机出车失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS机结算离场（POS机点击结算离场）")
    def out_settle(self, parkCode="", **kwargs):
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {"parkCode": parkCode}
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_OUT_SETTLE, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 车辆【{kwargs.get('carNo')}】通过POS机结算离场（POS机点击结算离场）成功！")
            return result_dic
        else:
            raise Exception(f"❌  车辆【{kwargs.get('carNo')}】通过POS机结算离场（POS机点击结算离场）失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("修改车牌/修改车型")
    def update_present_car(self, carNo, carType, parkspaceCode, parkCode="", **kwargs):
        """
        修改车牌/修改车型

        :param parkCode: 车场编码
        :param parkspaceCode: 要更新哪个车位的车牌
        :param carNo: 新车牌
        :param carType: 新车牌类型
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        carImg = FileService().uploadBase64(parkCode=parkCode, **kwargs).get('data')
        presentCars = self.get_presents(parkCode, **kwargs)['data']['roadPresentCars'][0]['presentCars']
        parkingRecordId = [car['parkingRecordId'] for car in presentCars if car['parkspaceCode'] == parkspaceCode][0]
        if not parkingRecordId:
            assert False, f'该车位：{parkspaceCode}没有车'
        test_data = {
                'carNo': carNo,
                'carType': carType,
                'parkingRecordId': parkingRecordId,
                'parkCode': parkCode,
                'carImg': carImg
            }
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_UPDATE_PRESENT_CAR, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 修改车辆【{carNo}】车牌/车型成功！")
            return result_dic
        else:
            raise Exception(f"❌ 修改车辆【{carNo}】车牌/车型）失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("现金支付成功（POS机现金支付）")
    def pay_success(self, orderNo, payTime, **kwargs):
        """
        现金支付成功（POS机现金支付） - /api/app/paySuccess

        :param payTime: 支付时间
        :param orderNo: 订单号
        """
        test_data = {"orderNo": orderNo,
                     "payTime": payTime
                     }
        kwargs.update(test_data)
        res = send_road_app_api(filepath.APP_PAY_SUCCESS, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 订单【{orderNo}】通过POS机现金支付成功！")
            return result_dic
        else:
            raise Exception(f"❌ 订单【{orderNo}】通过POS机现金支付失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("公共--POS机入车")
    def public_in_car(self, carNo, **kwargs):
        carType = kwargs['carType'] if kwargs.get('carType') or (kwargs.get('carType') == 0) else \
            generate_data.random_carType()
        kwargs.update({'carType': carType})
        if not carNo:
            carNo = generate_data.car_no()
        ret = self.register_in_car(carNo=carNo, **kwargs)
        time.sleep(0.5)
        return {
            'parkingRecordId': ret['data'],
            'carType': carType
        }

    @util.catch_exception
    @util.retry_fun
    @allure.step("公共--POS机直接离场")
    def public_out_car(self, **kwargs):
        if kwargs.get('outTime'):
            outTime = kwargs['outTime']
            kwargs.pop('outTime')
        else:
            outTime = generate_data.adjust_time(seconds=10)
        self.out(outTime=outTime, **kwargs), time.sleep(0.5)

    @util.catch_exception
    @util.retry_fun
    @allure.step("结算离场：查费 -> 结算离场")
    def fee_out_settle(self, carNo, parkingRecordId, tollmanId, queryFeeTime='', **kwargs):
        """
        结算离场：查费 -> 结算离场

        :param carNo:车牌号
        :param parkingRecordId:停车记录id
        :param tollmanId:收费员id
        :param queryFeeTime:离场时间
        """
        query_fee_data = {
            'parkingRecordId': parkingRecordId,
            'queryFeeTime': queryFeeTime
        }
        fee = self.get_fee(carNo, **query_fee_data)  # 查费（查费的响应信息要传到结算离场的请求参数中）
        isPayEscape = 1 if fee.get('totalEscape') else 0  # 是否欠费
        outSettle = self.out_settle(carNo=carNo, isPayEscape=isPayEscape, tollmanId=tollmanId, **fee, **kwargs)['data']
        return outSettle

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS机公共的结算离场方法（查费 -> 结算离场）")
    def public_fee_out_settle(self,carNo, parkingRecordId, outTime='', tollmanId="", **kwargs):
        """
        POS机公共的结算离场方法（查费 -> 结算离场）

        :param carNo: 车牌号
        :param parkingRecordId: 停车记录ID
        :param outTime: 出车时间/查费时间
        """
        tollmanId = tollmanId
        out_settle_fee = self.fee_out_settle(carNo, parkingRecordId, tollmanId, outTime, **kwargs)
        return out_settle_fee

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS机二维码支付（查询待缴账单 -> 下单 -> 模拟支付->查询支付结果）")
    def public_pos_qrcode_pay(self, carNo, payChannel=2, payType=99, orderType=1, settlementType=0, settlementWay=0,
                              **kwargs):
        """
        POS机二维码支付（查询待缴账单 -> 下单 -> 模拟支付->查询支付结果）

        :param carNo: 车牌号
        :param orderType: 订单类型(必填) 0:本次停车 1:欠费补缴（默认） 2:预支付 3:固定充值  (结算离场缴费和停车缴费都是0)
        :param settlementWay: 结算方式,0不使用预支付结算,1使用预支付金额结算
        :param settlementType: 结算类型 0:离场结算（不是在场车的结算） 1:在场结算
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        :param payType: 支付方式 0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他7:ETC99:聚合一码付
        """
        bills = self.get_bill(carNo)['data']  # 查询待缴订单
        if len(bills) == 0:
            logger.info(f'调试信息-查询车牌：{carNo}待缴账单信息如下：{bills}')
            raise Exception(f'未查询到车牌：{carNo}欠费订单')
        details = []
        for bill in bills:
            detail = {
                'totalMoney': bill['totalMoney'],  # 应收 = 实收 + 优惠
                'payMoney': bill['totalMoney'],  # 实收
                'freeMoney': bill['freeMoney'],  # 优惠
                'orderType': orderType,
                'originRecordId': bill['parkingRecordId']  # 本笔欠费的停车记录id
            }
            details.append(detail)
        parkingRecordIds = [detail['originRecordId'] for detail in details]
        parkingRecordIds = ','.join(parkingRecordIds)
        # TODO 缴历史 + 本次 ，detail应该由两部分组成
        # for detail in details:
        #     if detail.get('orderType') == 2:
        #         parkingRecordId = detail['originRecordId']
        #         break
        order_no = \
            self.order(carNo, details, parkingRecordIds, settlementType, settlementWay, payChannel, payType,
                       **kwargs)['data']['orderNo']
        pay = self.third_pay_query(order_no)
        assert pay['data']['status'] == 0, f'判断订单支付状态错误，理论值：待支付，实际结果：{pay}'
        mock_third_pay(carNo, order_no)
        pay = self.third_pay_query(order_no)
        assert pay['data']['status'] == 1, f'判断订单支付状态错误，理论值：已支付，实际结果：{pay}'
        return order_no

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS机停车缴费，勾选了欠费补缴【欠费+本次】（查本次费用，返回结果包含欠费信息 -> 下单 -> 模拟支付->查询支付结果）")
    def public_pos_qrcode_pay_escape_now(self, carNo, payChannel=2, payType=99, settlementType=1, settlementWay=1,
                                         parkingRecordId='', **kwargs):
        """
        POS机停车缴费，勾选了欠费补缴【欠费+本次】（查本次费用，返回结果包含欠费信息 -> 下单 -> 模拟支付->查询支付结果）

        :param carNo: 车牌号
        :param settlementWay: 结算方式,0不使用预支付结算,1使用预支付金额结算
        :param settlementType: 结算类型 0:离场结算（不是在场车的结算） 1:在场结算
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        :param payType: 支付方式 0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他7:ETC99:聚合一码付
        :param parkingRecordId: 在场车停车记录id
        """
        fee = self.get_fee(carNo=carNo, parkingRecordId=parkingRecordId)
        escape = fee['lacks']
        escape_details = []  # 存放欠费信息
        if escape:
            for i in escape:
                escape_detail = {'totalMoney': i['totalMoney'],
                                 'payMoney': i['totalMoney'],
                                 'freeMoney': i['freeMoney'],
                                 'originRecordId': i['parkingRecordId'],
                                 'orderType': i['historyEscape']
                                 }
                escape_details.append(escape_detail)
        unpaidTotal, unpaidPay, unpaidFree = 0, 0, 0
        if escape_details:
            for i in escape_details:
                unpaidTotal = unpaidTotal + i['totalMoney']
                unpaidPay = unpaidPay + i['payMoney']
                unpaidFree = unpaidFree + i['freeMoney']
            un_escape = {'unpaidTotal': unpaidTotal, 'unpaidPay': unpaidPay, 'unpaidFree': unpaidFree}
        # 本次停车费用信息
        detail = [{'totalMoney': fee['totalFee'] - fee['payMoney'],
                   'payMoney': fee['totalFee'] - fee['payMoney'],
                   'freeMoney': fee['freeMoney'],
                   'originRecordId': fee['parkingRecordId'],
                   'orderType': 0  # 本次
                   }]
        # 组装后的本次+欠费停车费用明细
        details = detail + escape_details
        parking_record_ids = [detail['originRecordId'] for detail in details]
        parking_record_ids = ','.join(parking_record_ids)
        order_no = \
            self.order(carNo, details, parking_record_ids, settlementType, settlementWay, payChannel, payType,
                       queryFeeTime=fee['queryFeeTime'], **un_escape, **kwargs)['data']['orderNo']
        pay = self.third_pay_query(order_no)
        assert pay['data']['status'] == 0, f'判断订单支付状态错误，理论值：待支付，实际结果：{pay}'
        mock_third_pay(carNo, order_no, amount=sum([i['totalMoney'] for i in details]))
        pay = self.third_pay_query(order_no)
        assert pay['data']['status'] == 1, f'判断订单支付状态错误，理论值：已支付，实际结果：{pay}'
        return order_no

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS预支付 - 预支付金额和停车费用相等")
    def public_pos_prepayment(self, carNo, payChannel=1, payType=0, parkingRecordId='', **kwargs):
        """
        POS预支付 - 预支付金额和停车费用相等

        :param carNo: 车牌号
        :param settlementWay: 结算方式,0不使用预支付结算,1使用预支付金额结算
        :param settlementType: 结算类型 0:离场结算（不是在场车的结算） 1:在场结算
        :param payChannel: 支付渠道 1:POS机3:停车小票4:速停车公众号5:公众号6:封闭停车场7:小程序8:APP9:ETC10:速停车运营端11:路内收费系统后台
        :param payType: 支付方式 0:现金1:微信2:支付宝3:银联4:线上转账5:优惠券6:其他7:ETC99:聚合一码付
        :param parkingRecordId: 在场车停车记录id
        """
        fee = self.get_fee(carNo=carNo, parkingRecordId=parkingRecordId)
        escape = fee['lacks']
        escape_details = []  # 存放欠费信息
        if escape:
            for i in escape:
                escape_detail = {'totalMoney': i['totalMoney'],
                                 'payMoney': i['totalMoney'],
                                 'freeMoney': fee['freeMoney']
                                 }
                escape_details.append(escape_detail)

        # 本次停车费用明细
        cur_detail = [{'totalMoney': fee['totalFee'] - fee['payMoney'],
                       'payMoney': fee['totalFee'] - fee['payMoney'],
                       'freeMoney': fee['freeMoney']
                       }]
        # 组装后的本次+欠费停车费用明细
        details = cur_detail + escape_details
        totalMoney, freeMoney, payMoney = 0, 0, 0
        if details:
            for i in details:  # 本次停车费用 + 历史的欠费
                totalMoney = totalMoney + i['totalMoney']
                payMoney = payMoney + i['payMoney']
                freeMoney = freeMoney + i['freeMoney']
            prepayment_detail = [
                {'payMoney': payMoney, 'totalMoney': totalMoney, 'freeMoney': freeMoney, 'orderType': 2,
                 'originRecordId': parkingRecordId}]
        # 下单
        order_no = \
            self.order(carNo, prepayment_detail, '', '', '', payChannel, payType, **kwargs)['data'][
                'orderNo']
        # 现金支付
        self.pay_success(order_no, fee['queryFeeTime'])
        return order_no

    @util.catch_exception
    @util.retry_fun
    @allure.step("POS预支付 - 预支付金额和停车费用相等")
    def judge_fixed_or_temp_car(self, record_id, expect, parking_info, **kwargs):
        """
        判断app详情页：临停车改为固定车之后的车位显示状态

        :param record_id: 停车记录ID
        :param expect: 预期值
        :param parking_info: 车场信息
        """
        count = 0
        while True:
            actual = self.get_present_detail(record_id, **parking_info)
            # 如果实际值跟预期值一样，返回True
            if actual['fixFlag'] == expect:
                return True
            time.sleep(0.7)
            count += 1
            if count == 3:  # 3次（3s）轮询之后，返回fasle
                logger.error(f'更改固定/临停车状态之后，查询是否为固定/临停车的轮询结果错误，详见：{actual}')
                return False


if __name__ == '__main__':
    carNo = "川AHJH789"
    parkspaceCode = "1"
    carType = "0"
    workstationId = "1462622751352295426"
    tollmanId = "1600422727436722177"
    parking_info = {'roadCode': 'road002350', 'tollmanId': '1676066840554631169',
                    'tollmanName': 'dwb007', 'workstationName': '自动化测试工作站',
                    'workstationId': '1676066842685337601', 'parkSpaceCode1': '1',
                    'parkSpaceCode2': '2', 'parkId': '1382254001977954305'}
    AppService().get_presents(**parking_info)