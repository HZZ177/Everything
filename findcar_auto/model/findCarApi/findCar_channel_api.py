#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:52
# @Author  : Heshouyi
# @File    : findCar_channel_api.py
# @Software: PyCharm
# @description: channel服务各个封装接口

import allure
import pytest
import requests
import uuid
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger

config = configger.load_config()


def park_enter(parklist: list, token):
    """
        入车接口
        :param token: 接口请求Token
        :param parklist: 入车的车位地址列表
        :return:响应参数的json格式
        """
    # 检查并添加新的Token到 header 中
    url = config.get('url').get('channel_url') + "/park/enter"
    headers = {
        'Accesstoken': token
    }
    params = {
        'list': parklist,
        'reqId': str(uuid.uuid4()).replace('-', '')
    }

    res = requests.post(url, headers=headers, json=params)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def park_leave(parklist: list, token):
    """
        入车接口
        :param token: 接口请求Token
        :param parklist: 出车的车位地址列表
        :return:响应参数的json格式
        """
    # 检查并添加新的Token到 header 中
    url = config.get('url').get('channel_url') + "/park/leave"
    headers = {
        'Accesstoken': token
    }
    params = {
        'list': parklist,
        'reqId': str(uuid.uuid4()).replace('-', '')
    }

    res = requests.post(url, headers=headers, json=params)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def park_updateplateno(addr, token, carimageurl, plateno, platenoreliability=900):
    """
    更新车牌号
    :param token: 接口请求Token
    :param addr: 需要更新车牌的车位地址
    :param carimageurl: 入车图片地址
    :param plateno: 入车车牌号
    :param platenoreliability: 入车车牌可信度，默认900
    :return:
    """
    # 检查并添加新的Token到 header 中
    url = config.get('url').get('channel_url') + "/park/updatePlateNo"
    headers = {
        'Accesstoken': token
    }
    params = {
        'list': [
            {
                "addr": addr,
                "carImageUrl": carimageurl,
                "plateNo": plateno,
                "plateNoReliability": platenoreliability
            }
        ],
        'reqId': str(uuid.uuid4()).replace('-', '')
    }

    res = requests.post(url, headers=headers, json=params)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')
