#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/10 下午2:07
# @Author  : Heshouyi
# @File    : encrypt.py
# @Software: PyCharm
# @description: 加密方法，用于寻车后台登录传参时加密明文密码

import rsa
import base64
from urllib.parse import quote


def encrypt_password(message):
    """
    寻车后台管理登录界面加密：原始密码加密顺序：密码明文-->rsa加密-->base64转码-->ut8转码-->经过http请求时自动url转码
    :param message:未加密的原始数据
    :return:原密码加密后的密文
    """
    # 定义原始公钥字符串
    public_key_str = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3aXGhT7IJgwjv09ripaeyqgFVg8Vnp4RzuDc9LCKJNyS7dmOUtotycjddQGLLVXnB3bM4YnLYyeVrQO1LZCJF9dlCw7y9PC/nZ50blCBGM6K0fh2NzEi30eyNi8k70PWmO/sf+VDvnezbfEp4pw+SwJpLZ820db3BP0IBSr9ybQIDAQAB\n-----END PUBLIC KEY-----\n"
    # 公钥字符串格式转换为公钥特殊格式，方便rsa加密调用
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_str.encode())
    # 使用公钥加密原始信息，得到rsa加密后的二进制字节串
    crypto_message = rsa.encrypt(message.encode(), public_key)
    # print(crypto_message)
    # 对rsa加密后的原始字节串进行base64编码，得到base64二进制字节串
    encoded_bytes = base64.b64encode(crypto_message)
    # base64二进制字节串转码为utf-8格式
    decoded_string = encoded_bytes.decode('utf-8')
    # print(decoded_string)
    # 可以直接返回加密字符不需要再转成url编码，get请求中会自动转
    return decoded_string


if __name__ == '__main__':
    # print(encrypt_password(message="keytop123456"))
    pass
