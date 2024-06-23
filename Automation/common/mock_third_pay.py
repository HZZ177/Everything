import hashlib
from time import strftime

from common.configLog import logger
from common.filepath import config
from common.generate_data import generate_data
from common.request import request

domain = config.get('app').get('domain')


def mock_third_pay(carNo, orderNo, amount=1, *args, **kwargs):
    """
    速停车支付成功回调

    :param orderNo: 下单方订单号
    :param carNo: 车牌号码
    :param amount: 支付金额
    """
    data = {
        'method': 'POST',
        'url': '/api/tpay/stc/PostStcPayResult',
        'json': {
            'amount': amount,
            'appId': '10300',
            'attach': '{\'paySource\':1}',
            'merOrderNo': 'TTPHN2021040178010140',
            'parkId': 5624,
            'payMethod': '00',
            'payTime': strftime('%Y-%m-%d %H:%M:%S'),
            'paymentTag': generate_data.g_uuid(),
            'plateNo': carNo,
            'reqId': generate_data.g_uuid(),
            'stcOrderNo': '000202104012161240',
            'ts': generate_data.time_to_unixTime_ms(),
            'ttpOrderNo': orderNo
        }
    }
    data['url'] = domain + data['url']
    if 'roadpark' in domain:
        data['json'].update({'parkId': 280028638, 'appId': '10408'})
    data['json']['key'] = tpay_sign(data['json'])

    resp = request.request(**data).json()


# 速停车签名
def tpay_sign(data: dict):
    secret = 'a9fb206b8e9844329861402905de07fa'
    if 'roadpark' in domain:
        secret = '63d3546af6404d08870001fbae93e3ca'
    data.pop('appId')

    data = dict(sorted(data.items(), key=lambda x: x[0]))
    sign_str = ''
    for key, value in data.items():
        if isinstance(value, int):
            value = str(value)
        sign_str = sign_str + key + '=' + value + '&'
    sign_str = sign_str + secret
    h1 = hashlib.md5()
    h1.update(sign_str.encode('utf-8'))
    sign = h1.hexdigest().upper()
    return sign


if __name__ == '__main__':
    mock_third_pay("川HJH789", "2322145465")