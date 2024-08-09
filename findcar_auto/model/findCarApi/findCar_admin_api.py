import allure
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


def get_lotinfo_byid(id: int, token=''):
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


def save_lotinfo(addr: str, defaultshowmaptype: int, deviceipprefix: str, id: int, lotcode: str, lotname: str, maptype: int, parkrepeatswitch: int, serverip: str, systemtype: int, tel: str, token=''):
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


def check_lotinfo(lotid: int, token=''):
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





if __name__ == '__main__':
    check_lotinfo(1)















