import requests


def login(url, header, params):
    """
    登录接口
    :param url: 登录接口地址
    :param header:请求头
    :param params:请求参数
    :return:响应参数的json格式
    """
    result = requests.get(url, headers=header, params=params)
    # print(result)
    message = result.json()
    # print(message)
    return message
