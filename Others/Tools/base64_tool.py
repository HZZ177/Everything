import base64


def encod_with_base64(target_str):
    """
    对目标字符串进行base64编码
    :param target_str:
    :return:
    """
    # 要编码的字符串
    string_to_encode = target_str
    # 对字符串进行 Base64 编码
    encoded_bytes = base64.b64encode(string_to_encode.encode('utf-8'))
    # 将编码后的字节串转换为字符串
    result = encoded_bytes.decode('utf-8')
    return result


def decoded_with_base64(target_string):
    """
    对目标字符串进行base64解码
    :param target_string:
    :return:
    """
    # 要解码的Base64编码字符串
    string_to_decode = target_string
    # 对Base64编码字符串进行解码
    decoded_bytes = base64.b64decode(string_to_decode)
    # 将解码后的字节串转换为字符串
    result = decoded_bytes.decode('utf-8')
    return result


if __name__ == '__main__':
    origin_string = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3aXGhT7IJgwjv09ripaeyqgFVg8Vnp4RzuDc9LCKJNyS7dmOUtotycjddQGLLVXnB3bM4YnLYyeVrQO1LZCJF9dlCw7y9PC/nZ50blCBGM6K0fh2NzEi30eyNi8k70PWmO/sf+VDvnezbfEp4pw+SwJpLZ820db3BP0IBSr9ybQIDAQAB"
