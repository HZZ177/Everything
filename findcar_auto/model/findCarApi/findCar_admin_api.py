import allure
import pytest
import requests
from findcar_auto.common.encrypt import encrypt_password
from findcar_auto.common.config_loader import configger
from findcar_auto.common.log_tool import logger

config = configger.load_config()


@allure.step("登录后台")
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
        if message['code'] != "200":
            logger.info(message)
            logger.info("接口请求成功但登录失败，请检查账号密码和验证码是否正确")
        else:
            logger.info(f"登录接口成功！")
        return message
    except Exception:
        logger.exception(f"登录接口返回信息格式化失败，请求结果：{res}，报错信息：")
        pytest.fail()
