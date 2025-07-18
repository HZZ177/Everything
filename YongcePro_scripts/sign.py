import hashlib
import json
from collections import OrderedDict


def params_sign(request_body, app_secret):
    """
    对字典类型的请求体进行签名
    """
    params = get_filter(request_body)
    # 拼接appSecret
    temp = '&'.join(f'{k}={v}' for k, v in params.items()) + '&' + app_secret
    print(f"拼接结果: {temp}")
    return md5(temp).upper()


def get_filter(request_body):
    """
    过滤请求体中的参数，只保留符合条件的参数
    """
    params = OrderedDict()  # 使用 OrderedDict 保证顺序
    for key, value in sorted(request_body.items()):  # 增加一个sorted来保证基础顺序
        if (key != "key" and
                key != "appId" and
                value is not None and
                not isinstance(value, dict) and
                not isinstance(value, list)):  # 区分 list 和 Iterable
            if str(value) != "":  # 转换为字符串再判断
                params[key] = str(value)  # 转换为字符串存储
    return params


def sign_key(request_body, app_secret):
    signature = params_sign(request_body, app_secret)
    print(f"签名结果: {signature}")
    request_body["key"] = signature
    print(json.dumps(request_body))


def flatten_json_for_signing(json_node, target_dict, level):
    """
    递归地平铺JSON对象。
    将所有在层级限制内的非对象键值对，全部收集到同一个目标字典中。
    这精确地模仿了Java代码将所有字段放入一个TreeMap前的收集步骤。
    """
    # 只有当当前节点是字典且层级未耗尽时才继续
    if not isinstance(json_node, dict) or level <= 0:
        return

    # 遍历当前层的所有键值对
    for key, value in json_node.items():
        if isinstance(value, dict):
            # 如果值是字典，则递归进入下一层
            flatten_json_for_signing(value, target_dict, level - 1)
        else:
            # 如果值是基本类型，则直接存入平铺的目标字典
            target_dict[key] = str(value)


def md5(data):
    """
    计算字符串的 MD5 哈希值。
    """
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


def sign(source, md5_key):
    json_string = json.dumps(source)
    json_node = json.loads(json_string)

    # 平铺：将所有符合条件的键值对收集到一个普通字典中。
    collected_fields = {}
    flatten_json_for_signing(json_node, collected_fields, 2)  # level=2 与Java代码一致

    # 排序：对平铺后的所有键进行一次全局字典序
    sorted_items = sorted(collected_fields.items())

    # 拼接：根据排序后的顺序构建签名字符串。
    sb_list = []
    for key, value in sorted_items:
        # 过滤掉指定的键，与Java代码一致
        if key not in ["customerRegionCode", "sign", "key"]:
            sb_list.append(value)

    # 将列表中的所有值连接成一个字符串，并附加md5_key
    final_string = "".join(sb_list) + md5_key

    # 4. 计算MD5
    result = md5(final_string).lower()

    print(f"拼接结果：{final_string}，\n签名结果：{result}")
    return result


def sign_key2(source_object, md5_key):
    signature2 = sign(source_object, md5_key)
    source_object["sign"] = signature2
    print(json.dumps(source_object))
    return json.dumps(source_object)


if __name__ == '__main__':
    request_body = {
        "appId": "1",
        "key": "",
        "msgMap": {},
        "openId": "",
        "reqId": "",
        "tmplNo": "",
        "topId": "",
        "ts": "",
        "url": "",
        "test": 123
    }
    app_secret = "4eb3b50d24f9469aa25214b9032b1202"

    # ---------------------------------------------
    source_object = {
        "errorCode": "",
        "errorDescription": "",
        "outRefundNo": "",
        "parameters": {
            "amount": 0,
            "category": "",
            "customParameters": {
                "billType": 0,
                "orderNo": "",
                "thirdOrderNo": "",
                "topId": "",
                "zone": ""
            },
            "id": "",
            "module": "",
            "operationType": "",
            "orderNo": "",
            "reason": "",
            "requestId": "",
            "sign": ""
        },
        "refundId": "",
        "refundMode": "",
        "refundTime": "",
        "requestId": "",
        "result": "",
        "sign": "",
        "test": 123
    }
    md5_key = "251fd1ef3e5d4cb4ba040aab9f94ca0d"

    # 适合 key 字段验签的加密方式
    # sign_key(request_body, app_secret)

    # 适合 sign 字段验签的加密方式
    result = sign_key2(source_object, md5_key).replace(" ", "")
    # 适合 pulsar的加密方式，用的就是sign字段的加密，只是组装成curl指令
    uri = ("http://localhost:27810/vehicle-mq-bridge/pulsar/send/message?topic=persistent://yongce-pro/"
           "owner-center/" +
           "temp-pay-callback")
    print("pulsar-curl组装：\n" + "curl -X POST " + f"-d{result} " + f"'{uri}'")