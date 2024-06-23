# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: ruleConfigService.py
@Description:
车场管理
    规则配置
        计费规则-新
        附加策略
        特殊日期管理
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/27
===================================
"""
import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import config
from model.road_park.road_toll_system_api import send_road_toll_system_api


class RuleConfigService:
    """
    车场管理之规则配置模块下的 api service
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("添加计费规则")
    def add_rule_group(self, ruleName, feeRuleGroupDesc, fixFeeType: int = 0, dateFeeType: int = 0, periodType: int = 0,
                       periodCapFeeYuan: str = '0', freeType: int = 0, freeTimeMin: int = 0, affiliateType: int = 0,
                       freeTimes=0, timeBegin: str = '00:00:00', timeEnd: str = '24:00:00', timeCapFeeYuan: str = '0',
                       feeRuleTimeDetails=None, isSameToSmall=1, parkCode="", **kwargs):
        """
        新增计费规则 （免费5min，最多0.01）

        :param fixFeeType: 计费车型：0 临停车（默认临停车）
        :param ruleName: 计费规则名称
        :param feeRuleGroupDesc: 计费规则描述
        :param dateFeeType: 规则适用 0 周一到周日（默认）；1 工作日；2 休息日；3 节假日 4 特殊日
        :param periodType: 计费周期：0：自然天（默认），1：24小时
        :param periodCapFeeYuan: 周期封顶金额 默认0
        :param freeType: 是否固免: 0: 超过不免（默认），1：固定减免
        :param freeTimeMin: 免费时长 分: 默认0
        :param affiliateType: 跨靠配置：0：不靠（默认），1：前靠
        :param freeTimes: 免费时间次数：0：每次停车都享受（默认），2：自然天仅享受一次
        :param timeBegin: 时段开始时间：默认00:00
        :param timeEnd: 时段结束时间：默认24:00
        :param timeCapFeeYuan: 时段封顶金额：默认0
        :param feeRuleTimeDetails: 计费时间段明细
        :param isSameToSmall: 是否与小型车一致，0不一致（默认），1一致
        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        if feeRuleTimeDetails is None:
            feeRuleTimeDetails = [{  # 前计时
                'durationMin': '1',  # 停留多少分钟
                'durationFeeYuan': '2',  # 收费多少元
                'isAffiliateStart': 1,  # 从此段开始（前计时/循环计时），1表示从此段开始
                'serialNum': 0  # 计费序列号，前计时从0开始递增，-1表示循环计时
            }, {  # 循环计时
                'durationMin': '3',
                'durationFeeYuan': '4',
                'isAffiliateStart': 0,
                'serialNum': -1
            }]
        test_data = {
            'feeRuleGroupName': ruleName,
            'feeRuleGroupDesc': feeRuleGroupDesc,
            'parkCode': parkCode,
            'feeRules': [{
                'carType': 0,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }, {
                'carType': 1,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }, {
                'carType': 2,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }, {
                'carType': 3,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }, {
                'carType': 4,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }, {
                'carType': 5,
                'dateFeeType': dateFeeType,
                'affiliateType': affiliateType,
                'fixFeeType': fixFeeType,
                'freeTimeMin': freeTimeMin,
                'freeTimes': freeTimes,
                'freeType': freeType,
                'isSameToSmall': isSameToSmall,
                'periodCapFeeYuan': periodCapFeeYuan,
                'periodType': periodType,
                'parkCode': parkCode,
                'feeRuleTimes': [{
                    'isOpen': True,
                    'timeBegin': timeBegin,
                    'timeEnd': timeEnd,
                    'timeCapFeeYuan': timeCapFeeYuan,
                    'feeRuleTimeDetails': feeRuleTimeDetails
                }]
            }]
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_ADD_PARKING_RULE_GROUP, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 增加车场【{parkCode}】计费规则【{ruleName}】成功！")
        return result_dic

    @util.catch_exception
    @util.retry_fun
    @allure.step("删除计费规则")
    def delete_rule_group(self, ruleName='', parkCode="", **kwargs):
        """
        删除计费规则

        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        if kwargs.get('fee_id'):
            fee_id = kwargs['fee_id']
        else:
            rules = self.get_rule_group_page()['data']['records']
            fee_id = [rule['id'] for rule in rules if rule['feeRuleGroupName'] == ruleName][0]
            assert fee_id, f'没有该计费规则 {ruleName}'
        test_data = {
            "id": fee_id
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_DEL_PARKING_RULE_GROUP, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 删除车场【{parkCode}】计费规则【{fee_id}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 删除车场计费规则失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("分页查询计费规则组")
    def get_rule_group_page(self, parkCode="", **kwargs):
        """
        分页查询计费规则组

        :param parkCode: 车场编码
        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        test_data = {
            "parkCode": parkCode
        }
        kwargs.update(test_data)
        res = send_road_toll_system_api(filepath.MANAGE_GET_PARKING_RULE_GROUP_INFO, 1, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 查询车场【{parkCode}】计费规则成功！")
            return result_dic
        else:
            raise Exception(f"❌ 查询车场计费规则失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("计费规则批量绑定路段")
    def fee_batch_bind(self, ruleName, roadCode, parkCode="", **kwargs):
        """
        :param ruleName: 计费规则名字
        :param parkCode: 车场编码
        :param roadCode: 路段名字

        """
        parkCode = parkCode if parkCode else config.get("parkCode")
        rules = self.get_rule_group_page(size=20)['data']['records']
        fee_id = [rule.get('id') for rule in rules if rule.get('feeRuleGroupName') == ruleName][0]
        assert fee_id, f'没有该计费规则 {ruleName}'
        base = {
            'feeRuleGroupId': fee_id,
            'parkCode': parkCode
        }
        if isinstance(roadCode, list):
            data = []
            [data.append({'roadCode': i}) for i in roadCode]
            [i.update(base) for i in data]
        else:
            base['roadCode'] = roadCode
            data = [base]
        test_data = {"json": data
                     }
        res = send_road_toll_system_api(filepath.MANAGE_BATCH_BIND_PARKING_RULE, 1, header_data={}, test_data=test_data,
                                        custom_param_type=1)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 绑定车场【{parkCode}】路段【{roadCode}】计费规则【{ruleName}】成功！")
            return result_dic
        else:
            raise Exception(f"❌ 绑定车场计费规则失败！错误为【{result_dic}】!")

    @util.catch_exception
    @util.retry_fun
    @allure.step("获取计费规则id")
    def get_fee_id(self, ruleName, *args, **kwargs) -> str:
        """
        获取计费规则id

        :param ruleName: 计费规则名字
        """
        records = self.get_rule_group_page(size=30, *args, *kwargs)['data']['records']
        fee_id = [record['id'] for record in records if record.get('feeRuleGroupName') == ruleName][0]
        assert fee_id, f'无此计费规则 {ruleName}'
        return fee_id


if __name__ == '__main__':
    ruleName = '自动化测试计费规则'
    # RuleConfigService().add_rule_group(ruleName, ruleName, periodCapFeeYuan='0.01', freeTimeMin=5)
    # RuleConfigService().get_rule_group_page()
    RuleConfigService().fee_batch_bind(ruleName, "road001252")
