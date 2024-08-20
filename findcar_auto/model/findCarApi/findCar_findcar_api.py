#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:52
# @Author  : Heshouyi
# @File    : findCar_findcar_api.py
# @Software: PyCharm
# @description: findcar服务各个封装接口

import requests
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger

config = configger.load_config()


def device_cmd(lightcmdfordpsreq: str = '', token: str = ''):
    """
    cmd指令
    :param str lightcmdfordpsreq: lightCmdForDpsReq
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/cmd'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'lightCmdForDpsReq': lightcmdfordpsreq,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_gdlamp(cmd: str = None, list: list = None, reqid: str = None, token: str = ''):
    """
    探测器车位灯
    :param str cmd: 暂无参数描述
    :param list list: 暂无参数描述
    :param str reqid: 暂无参数描述
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/gdlamp'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'cmd': cmd,
        'list': list,
        'reqId': reqid,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_getallonlinedeviceinfo(token: str = ''):
    """
    获取当前所有在线设备数据
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/getAllOnLineDeviceInfo'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_getlcdscreendata(ipandtype: str = None, token: str = ''):
    """
    获取LCD屏下发数据
    :param str ipandtype: ipAndType
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/getLcdScreenData'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'ipandtype': ipandtype,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_getlcdscreenonlinestatus(ipandtype: str = None, token: str = ''):
    """
    获取LCD屏设备在线状态(0-离线，1-在线)
    :param str ipandtype: ipAndType
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/getLcdScreenOnlineStatus'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'ipandtype': ipandtype,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_getregistrationinfo(token: str = ''):
    """
    注册文件信息查询接口
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/getRegistrationInfo'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_lamp(cmd: str = None, list: list = None, reqid: str = None, token: str = ''):
    """
    dsp车位灯
    :param str cmd: 暂无参数描述
    :param list list: 暂无参数描述
    :param str reqid: 暂无参数描述
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/lamp'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'cmd': cmd,
        'list': list,
        'reqId': reqid,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_ledcommandnode(addr: int = None, channeltype: int = None, controlcode: str = None, screencategory: int = None, shownum: int = None, token: str = ''):
    """
    屏更新指令
    :param int addr: 屏地址
    :param int channeltype: 渠道类型:1：tcp 2：node-tcp 3：node-485
    :param str controlcode: 屏控制字
    :param int screencategory: 屏类别 1：LED网络屏   2：485总屏、3：485子屏
    :param int shownum: 展示数字
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/ledCommandNode'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'addr': addr,
        'channelType': channeltype,
        'controlCode': controlcode,
        'screenCategory': screencategory,
        'showNum': shownum,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_log(level: str = '', token: str = ''):
    """
    当前服务中日志类型存在冲突，该接口咋不可用
    :param str level: level
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/log'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'level': level,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def call_recognition(url: str = '', token: str = ''):
    """
    识别库调用接口
    :param str url: url
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/recognitionTest'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'url': url,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口请求失败，请求结果：{res}，报错信息：')


def device_sendlcdscreendata(cmd: str = None, data: str = None, ip: str = None, reqid: str = None, scene: str = None, ts: int = None, type: int = None, token: str = ''):
    """
    指令下发LCD屏数据
    :param str cmd: 暂无参数描述
    :param str data: 暂无参数描述
    :param str ip: 暂无参数描述
    :param str reqid: 暂无参数描述
    :param str scene: 暂无参数描述
    :param int ts: 暂无参数描述
    :param int type: 暂无参数描述
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/sendLcdScreenData'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'cmd': cmd,
        'data': data,
        'ip': ip,
        'reqid': reqid,
        'scene': scene,
        'ts': ts,
        'type': type,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_sendlcdscreendatabatch(lcdsocketmessagelist: str = '', token: str = ''):
    """
    指令下发LCD屏数据
    :param str lcdsocketmessagelist: lcdSocketMessageList
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/sendLcdScreenDataBatch'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'lcdSocketMessageList': lcdsocketmessagelist,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_snappicture(addrlist: list = None, testingbatchid: str = None, token: str = ''):
    """
    相机抓拍接口
    :param list addrlist: 车位地址
    :param str testingbatchid: 质检中心检测批次ID
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/snapPicture'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'addrList': addrlist,
        'testingBatchId': testingbatchid,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_tankwarncommand(wavcmdlist: str = '', token: str = ''):
    """
    语音播放指令
    :param str wavcmdlist: wavCmdList
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/tankWarnCommand'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'wavCmdList': wavcmdlist,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_updatefindcarstatusswitch(statusswitch: int = '', token: str = ''):
    """
    紧急-找车系统车位状态上报接口开关(0：关闭，1：开启)
    :param int statusswitch: statusSwitch
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/updateFindCarStatusSwitch'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'statusswitch': statusswitch,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_updatenodedeviceissue(token: str = ''):
    """
    更新当前485节点设备数据下发
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/updateNodeDeviceIssue'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')


def device_warninfocommand(addr: int = None, channeltype: int = None, controlcode: str = None, screencategory: int = None, shownum: int = None, token: str = ''):
    """
    告警指令
    :param int addr: 屏地址
    :param int channeltype: 渠道类型:1：tcp 2：node-tcp 3：node-485
    :param str controlcode: 屏控制字
    :param int screencategory: 屏类别 1：LED网络屏   2：485总屏、3：485子屏
    :param int shownum: 展示数字
    :param token: 接口请求Token
    """
    url = config.get('url').get('findcar_url') + '/device-access/device/warnInfoCommand'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'addr': addr,
        'channelType': channeltype,
        'controlCode': controlcode,
        'screenCategory': screencategory,
        'showNum': shownum,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回失败，请求结果：{res}，报错信息：')
