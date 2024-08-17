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
    url = config.get('url').get('admin_url') + "/auth/login"
    headers = {
        'Cookie': f'JSESSIONID={jsessionid}',
    }
    params = {
        'account': config.get('account').get('username'),
        'password': encrypt_password(message=config.get('account').get('password')),
        'verifyCode': verify_code
    }

    res = requests.get(url, headers=headers, params=params)
    try:
        message = res.json()
        if message['message'] != "成功":
            logger.info(f"登录失败，接口返回message:{message['message']}")
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
    url = config.get('url').get('admin_url') + '/lot-info/getById'
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
    url = config.get('url').get('admin_url') + '/lot-info/save'
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
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def check_lotinfo_configure(lotid: int, token=''):
    """
    车场配置检测
    :param int lotid: lotId
    :param token: 接口请求Token
    """
    url = config.get('url').get('admin_url') + '/lot-info/lotInfoCheck'
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
    url = config.get('url').get('admin_url') + '/floorInfo/selectPageList'
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
    url = config.get('url').get('admin_url') + '/areaInfo/selectPageList'
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
    url = config.get('url').get('admin_url') + '/deviceInfo/selectPageList'
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
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def align_devices(token=''):
    """
    设备列表校准
    :param token: 接口请求Token
    """
    url = config.get('url').get('admin_url') + '/deviceInfo/deviceListAlign'
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
    url = config.get('url').get('admin_url') + '/deviceInfo/exportDeviceList'
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
    return res


def query_verifycode(token: str = ''):
    """
    生成图形验证码
    :param token: 接口请求Token
    """
    url = config.get('url').get('admin_url') + '/auth/verifyCode'
    headers = {
        'Accesstoken': f'{token}'
    }
    params = {
    }
    res = requests.request('GET', url, params=params, headers=headers)
    return res


def query_history_car_in_out_record(areaname: str = None, floorid: int = None, id: int = None, inendtime: str = None, instarttime: str = None, intype: int = None, lotid: int = None, outendtime: str = None, outstarttime: str = None, outtype: int = None, pagenumber: int = None, pagesize: int = None, parkno: str = None, plateno: str = None, token: str = ''):
    """
    历史进出车记录 分页查询
    :param str areaname: 区域名称
    :param int floorid: 楼层id
    :param int id: 记录id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-自动入车 1-手动入车
    :param int lotid: 车场id
    :param str outendtime: 出车结束时间
    :param str outstarttime: 出车开始时间
    :param int outtype: 操作类型 0-自动出车 1-手动出车
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkno: 车位号
    :param str plateno: 车牌号
    :param token: 接口请求Token
    """
    url = config.get('url').get('admin_url') + '/car-in-out-record/selectPageList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'areaName': areaname,
        'floorId': floorid,
        'id': id,
        'inEndTime': inendtime,
        'inStartTime': instarttime,
        'inType': intype,
        'lotId': lotid,
        'outEndTime': outendtime,
        'outStartTime': outstarttime,
        'outType': outtype,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'parkNo': parkno,
        'plateNo': plateno,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


def query_realtime_parkinfo(areaname: str = None, elementparkcontrol: int = None, floorid: int = None, inendtime: str = None, instarttime: str = None, intype: int = None, lotid: int = None, pagenumber: int = None, pagesize: int = None, parkaddr: str = None, parkno: str = None, parkstatus: int = None, plateno: str = None, specialdata: int = None, token: str = ''):
    """
    分页查询 - 实时车位报表
    :param str areaname: 区域名称
    :param int elementparkcontrol: 车位控制状态 默认为空查全部，下拉选择： 0 自动控制、1 手动控制
    :param int floorid: 楼层id
    :param str inendtime: 进车结束时间
    :param str instarttime: 进车开始时间
    :param int intype: 操作类型 0-系统进车 1-手动进车
    :param int lotid: 车场id
    :param int pagenumber: 页数
    :param int pagesize: 每页条目数
    :param str parkaddr: 车位地址
    :param str parkno: 车位号
    :param int parkstatus: 车位状态
    :param str plateno: 车牌号
    :param int specialdata: 特殊数据筛选查询，默认为空查全部，下拉选择：1:编号重复车位（查询系统内楼层-区域-编号重复的车位）；2:地址重复车位（查询系统车位地址重复的车位）；3:车牌识别失败车位（系统进车，占用状态但车牌为空）
    :param token: 接口请求Token
    """
    url = config.get('url').get('admin_url') + '/present-car-record/selectPageList'
    headers = {
        'Accesstoken': f'{token}'
    }
    data = {
        'areaName': areaname,
        'elementParkControl': elementparkcontrol,
        'floorId': floorid,
        'inEndTime': inendtime,
        'inStartTime': instarttime,
        'inType': intype,
        'lotId': lotid,
        'pageNumber': pagenumber,
        'pageSize': pagesize,
        'parkAddr': parkaddr,
        'parkNo': parkno,
        'parkStatus': parkstatus,
        'plateNo': plateno,
        'specialData': specialdata,
    }
    res = requests.request('POST', url, json=data, headers=headers)
    try:
        message = res.json()
        if message['message'] != '成功':
            logger.info(f'接口返回失败，接口返回message：{message['message']}')
        return message
    except Exception:
        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')


if __name__ == '__main__':
    pass
    # get_verifycode()
