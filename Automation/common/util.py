import base64
import datetime
# from common import filepath, encryption
import json
import os
import random
import time
import traceback
from functools import wraps

import rsa
from jsonpath_rw import parse

from common import filepath
from common.configLog import logger


def generate_car(is_special=False):
    """
    随机生成车牌
    parameter:
        is_special: 生成特殊车牌传True，默认为False
    return:
        car_no: 随机生成的车牌
    """
    province = '京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽赣粤青藏川宁琼'
    letter = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    numbers = '0123456789'
    car_no = ""
    car_no += province[random.randint(1, len(province) - 1)]
    car_no += letter[random.randint(1, len(letter) - 1)]
    for i in range(4):
        car_no += numbers[random.randint(1, len(numbers) - 1)]
    end_str = "军" if is_special else numbers[random.randint(1, len(numbers) - 1)]
    car_no += end_str
    logger.info("随机生成车牌：%s" % car_no)
    return car_no


def check_recv(recv_list, need_in=True):
    """
    检测dsp返回数据是否开闸，收到R指令
    parameter:
        recv_list: 接受消息列表
        need_in: 车辆需要入场为True,不需要为False
    return:
    """
    temp = False
    for msg in recv_list:
        if '收到R指令' in msg:
            logger.info("dsp收到R指令，开闸")
            temp = True
    if not temp:
        logger.info("dsp没有收到R指令，没有开闸")
    if need_in == temp:
        logger.info("✔ 校验成功")
    else:
        raise Exception(logger.error('校验失败'))


def check_result(func):
    """
    校验函数返回值是否与预期值一致
    """

    @wraps(func)
    def inner(*args, **kwargs):
        """
        :param args:
        :param kwargs: expect，预期结果，不传直接校验函数返回值
                       wrapper_wait_time，校验装饰器等待时间，不传直接返回函数值
        :return:
        """
        wait_time = kwargs.get("wrapper_wait_time")
        if wait_time is None or not isinstance(wait_time, int):
            return func(*args, **kwargs)
        else:
            endtime = datetime.datetime.now() + datetime.timedelta(seconds=wait_time)
            expect = kwargs.get("expect")
            ret = False
            while datetime.datetime.now() < endtime:
                ret = func(*args, **kwargs)
                if expect is not None:
                    if ret == expect:
                        break
                else:
                    if ret:
                        break
                time.sleep(1)
            return ret

    return inner


def catch_exception(func):
    """捕获异常写入日志"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise Exception(logger.error(traceback.format_exc()))

    return wrapper


@catch_exception
def retry_fun(func):
    """失败重试，setting文件中配置，默认3次"""

    def wrapper(*args, **kwargs):
        temp = True  # 打印日志标记
        if kwargs.get('no_log'):
            temp = False
            kwargs.pop('no_log')
        num = int(filepath.config.get("retry_num"))
        i = 1
        while i < num + 1:
            try:
                if temp:
                    logger.info("第%s次，进行%s" % (i, func.__name__))
                res = func(*args, **kwargs)
                return res
            except Exception as msg:
                logger.error(traceback.format_exc())
                i += 1
                time.sleep(1)
        logger.error(f"请求失败{num}次！请求函数:%s" % func.__name__)

    return wrapper


@catch_exception
def get_json_data_by_path(v, data):
    """
    处理响应数据，主要是从响应数据中获取依赖需要的数据
    :param v: 依赖的字段，如 test_id:data.uuid 表示依赖其他用例的参数是uuid, 然后uuid的层级是data.uuid
    :param data: 对应依赖用例的响应体
    :return: 从依赖用例的响应体中提取出的对应依赖字段的数据
    """
    json_exe = parse(v)
    if not isinstance(data, dict):
        data = json.loads(data)
    try:
        result = [match.value for match in json_exe.find(data)][0]
        return result
    except TypeError:
        raise ValueError(logger.error('未能获取有效参数或给予的JSON路径不对，请检查参数设置！'))


@logger.catch
def format_request_data_extend(request_data: dict):
    """
    根据需要处理用例中的依赖项，这里主要处理 session
    当然通过在用例中利用模板 ${} 来自定义参数，也可以实现其他更复杂的依赖
    :param request_data:
    :return:
    """
    if not request_data:
        return request_data
    for i, v in request_data.items():
        if "$j" in str(v):
            v = v.replace("$j{", "", 1).replace("}", "", 1)
            case_path, json_path = v.split(":")
            test_data = get_data_from_json_file(case_path, filepath.TESTDATAFILE)
            request_data[i] = get_json_data_by_path(json_path, test_data)
    return request_data


def save_response_to_json_file(id, res, path=filepath.TOKEN_FILE):
    """
    将redis中的token查询出来储存起来
    :param path: 储存文件地址
    :param id: token key值
    :param res: token
    :return:
    """
    new_data = {id: res}
    # 如果 json 文件不存在，则创建
    if not os.path.exists(path):
        with open(path, 'w'):
            pass
    with open(path, 'r') as j:
        try:
            comment = json.load(j)
        except json.decoder.JSONDecodeError:
            comment = new_data
        if comment:
            comment.update(new_data)
    with open(path, 'w') as j:
        json.dump(comment, j, ensure_ascii=False, indent=4)
    with open(path, "r") as j:
        comment = json.load(j)
        logger.info(f"存储code成功json文件信息为{comment}")


def get_data_from_json_file(key, path=filepath.TOKEN_FILE):
    """
    从 json 文件中读取数据
    以用例ID为key，读取该用例执行后的Response，用作其他用例的依赖
    :param path:
    :param key:
    :return:
    """
    with open(path) as j:
        comment = json.load(j)
        return comment.get(key)


def encrypt_text(password, path=filepath.PUBLIC_KEY):
    """
    登录客户端用户密码加密

    :param password: 密码，明文
    :param path: 文件路径
    :return: 加密后的字符串
    """
    # 公钥字符串，一般该公钥会由服务端给出
    with open(path) as f:
        public_key = f.read()
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key.encode())
    # 公钥加密
    encrypted_text = rsa.encrypt(password.encode('utf-8'), pubkey)
    return base64.b64encode(encrypted_text).decode()


if __name__ == "__main__":
    pass
