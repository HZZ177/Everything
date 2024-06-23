import time

import requests

from common import filepath, util
from common.configLog import logger

ocr_domain = 'https://aip.baidubce.com'
baidu_token_tag = "baidu_token"


def get_code(base_img):
    """
    base64编码的图片通过百度OCR识别

    :param base_img: 图片的base64编码字符串
    """
    while True:
        access_token = get_access_token()
        params = {
            'image': base_img,
            'access_token': access_token
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(f'{ocr_domain}/rest/2.0/ocr/v1/accurate_basic', data=params, headers=headers).json()
        logger.info(f'调试信息-百度ocr识别返回结果：{response}')
        if response.get('error_code'):
            util.save_response_to_json_file(baidu_token_tag, ["", 0])
        else:
            break
    word: str = response['words_result'][0]['words']
    logger.info(f'百度识别后的验证码为：{word}')
    word = word.replace(' ', '')
    return word


def get_access_token():
    baidu_token_info = util.get_data_from_json_file(baidu_token_tag)
    if baidu_token_info and baidu_token_info[0]:
        accessToken = baidu_token_info[0]
        expireTimes = baidu_token_info[1]
        if accessToken and expireTimes > int(time.time()) + 60 * 60 * 24:
            return accessToken
    baidu_info = filepath.config.get("baidu_ocr_api")
    host = f'{ocr_domain}/oauth/2.0/token?'
    params = {
        'grant_type': 'client_credentials',
        'client_id': baidu_info['client_id'],
        'client_secret': baidu_info['client_secret']
    }
    response = requests.get(host, params=params)
    logger.info(f'调试信息-百度ocr获取的token信息：{response.json()}')
    if response.status_code != 200:
        raise Exception('百度ocr识别出错,请检查config.yml文件中的baidu_ocr_api')
    baidu_token = response.json()['access_token']
    expireTimes = int(time.time()) + 60 * 60 * 24 * 7
    util.save_response_to_json_file(baidu_token_tag, [baidu_token, expireTimes])
    return baidu_token


if __name__ == '__main__':
    pass
