#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/30 下午10:52
# @Author  : Heshouyi
# @File    : findCar_admin_api.py
# @Software: PyCharm
# @description: admin服务各个封装接口

import pytest
import requests
from findcar_auto.common.encrypt import encrypt_password
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger

config = configger.load_config()


def login(verify_code, jsessionid=''):
    """
    登录接口
    :param jsessionid: 框架下发的jsessionid，用于绑定该次登录行为和验证码
    :param verify_code: 验证码
    :return:响应参数的json格式
    """
    url = config['url']['admin_url'] + "/auth/login"
    headers = {
        'Cookie': f'JSESSIONID={jsessionid}',
    }
    params = {
        'account': config['account']['username'],
        'password': encrypt_password(message=config['account']['password']),
        'verifyCode': verify_code
    }

    res = requests.get(url, headers=headers, params=params)
    try:
        message = res.json()
        if message['message'] != "成功":
            logger.info(f"接口请求成功但登录失败，接口返回message:{message['message']}")
        else:
            logger.info(f"登录接口成功！")
        return message
    except Exception:
        logger.exception(f"登录接口返回信息格式化失败，请求结果：{res}，报错信息：")
        pytest.fail()


def query_lotinfo_byid(id: int, token=''):
    """
    根据主键获取详情
    :param int id: 主键
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/lot-info/getById'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'id': id,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def save_lotinfo(addr: str, defaultshowmaptype: int, deviceipprefix: str, id: int, lotcode: str, lotname: str,
                 maptype: int, parkrepeatswitch: int, serverip: str, systemtype: int, tel: str, token=''):
    """
    保存
    :param str addr: 车场地址
    :param int defaultshowmaptype: 默认展示地图类型 2=2D地图，3=3D地图
    :param str deviceipprefix: 设备IP网段前缀
    :param int id: 楼层id
    :param str lotcode: 车场编码
    :param str lotname: 车场名称
    :param int maptype: 地图类型 0:2D地图 1:3D地图
    :param int parkrepeatswitch: 车位编号限制 0:不允许重复的车位编号  1:允许重复车位编号
    :param str serverip: 服务器IP
    :param int systemtype: C++端部署形式  1:引导系统  2:找车系统  3:引导系统和找车系统同时部署
    :param str tel: 联系电话
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/lot-info/save'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'addr': addr,
        'defaultshowmaptype': defaultshowmaptype,
        'deviceipprefix': deviceipprefix,
        'id': id,
        'lotcode': lotcode,
        'lotname': lotname,
        'maptype': maptype,
        'parkrepeatswitch': parkrepeatswitch,
        'serverip': serverip,
        'systemtype': systemtype,
        'tel': tel,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def check_lotinfo_configure(lotid: int, token=''):
    """
    车场配置检测
    :param int lotid: lotId
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/lot-info/lotInfoCheck'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
        'lotId': lotid,
    }
    res = requests.request('GET', url, params=params, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def query_floorinfo(endtime: str = '', floorname: str = '', flooruniqueidentification: str = '', id: int = '', lotid: int = '', pagenumber: int = '', pagesize: int = '', sort: int = '', starttime: str = '', status: int = '', token=''):
    """
    分页查询
    :param str endtime: 开始时间
    :param str floorname: 楼层名称
    :param str flooruniqueidentification: 楼层唯一标识字段
    :param int id: 楼层id
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int sort: 楼层顺序
    :param str starttime: 开始时间
    :param int status: 启用状态 1启用 2停用
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/floorInfo/selectPageList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'endTime': endtime,
        'floorName': floorname,
        'floorUniqueIdentification': flooruniqueidentification,
        'id': id,
        'lotId': lotid,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'sort': sort,
        'startTime': starttime,
        'status': status,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def query_areainfo(areaid: int = None, areaname: str = None, endtime: str = None, floorid: int = None, lotid: int = None, pagenumber: int = None, pagesize: int = None, starttime: str = None, type: int = None, token=''):
    """
    查询区域列表
    :param int areaid: id
    :param str areaname: 名称
    :param str endtime: 结束时间
    :param int floorid: 楼层id
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str starttime: 开始时间
    :param int type: 0:普通区域 1:立体车库区域
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/areaInfo/selectPageList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'areaId': areaid,
        'areaName': areaname,
        'endTime': endtime,
        'floorId': floorid,
        'lotId': lotid,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'startTime': starttime,
        'type': type,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def query_deviceinfo(deviceaddrip: str = None, devicetype: int = None, id: int = None, nodedeviceaddr: str = None, onlinestatus: int = None, pagenumber: int = None, pagesize: int = None, protocoltype: int = None, workingstatus: int = None, token=''):
    """
    设备列表分页查询
    :param str deviceaddrip: 设备地址（IP或者拨码）
    :param int devicetype: 设备类型 0=未知  1=车位相机  2=超声波探测器  3=LED屏  4=找车机  5=车位灯 6 LCD屏  7节点设备
    :param int id: 主键id
    :param str nodedeviceaddr: 节点设备地址
    :param int onlinestatus: 在线状态  0=离线  1=在线
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int protocoltype: 设备协议类型
    :param int workingstatus: 工作状态  0=故障  1=正常
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/deviceInfo/selectPageList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'deviceAddrIp': deviceaddrip,
        'deviceType': devicetype,
        'id': id,
        'nodeDeviceAddr': nodedeviceaddr,
        'onlineStatus': onlinestatus,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'protocolType': protocoltype,
        'workingStatus': workingstatus,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def align_devices(token=''):
    """
    设备列表校准
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/deviceInfo/deviceListAlign'
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
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def export_deviceList(deviceaddrip: str = None, devicetype: int = None, id: int = None, nodedeviceaddr: str = None, onlinestatus: int = None, pagenumber: int = None, pagesize: int = None, protocoltype: int = None, workingstatus: int = None, token=''):
    """
    设备列表导出
    :param str deviceaddrip: 设备地址（IP或者拨码）
    :param int devicetype: 设备类型 0=未知  1=车位相机  2=超声波探测器  3=LED屏  4=找车机  5=车位灯 6 LCD屏  7节点设备
    :param int id: 主键id
    :param str nodedeviceaddr: 节点设备地址
    :param int onlinestatus: 在线状态  0=离线  1=在线
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param int protocoltype: 设备协议类型
    :param int workingstatus: 工作状态  0=故障  1=正常
    :param token: 接口请求Token
    """
    url = config['url']['admin_url'] + '/deviceInfo/exportDeviceList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'deviceAddrIp': deviceaddrip,
        'deviceType': devicetype,
        'id': id,
        'nodeDeviceAddr': nodedeviceaddr,
        'onlineStatus': onlinestatus,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'protocolType': protocoltype,
        'workingStatus': workingstatus,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        else:
            logger.info(f'接口返回成功！')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')

