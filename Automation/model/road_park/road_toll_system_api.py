# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: road_hard_ware_camera_api.py
@Description: 请求路侧收费系统接口
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/05/31
===================================
"""
import json

from common import filepath, util
from common.processYaml import Yaml
from common.request import request


def send_road_toll_system_api(yaml_path, model, header_data, test_data, custom_param_type=0, timeout=10):
    """
    请求路侧收费系统接口
    :param yaml_path: 接口yaml文件路径
    :param model: yaml解析模式
    :param header_data: 请求头数据
    :param test_data: 测试数据
    :param custom_param_type: 是否自定义传参
    :param timeout: 超时时间 默认10
    :return:
    """
    read_data = Yaml(yaml_path, model)
    url = read_data.url
    method = read_data.method
    datas = read_data.allData
    headers = read_data.headers
    headers.update(header_data if header_data else {})
    headers['Code'] = util.get_data_from_json_file("Code")
    if not headers.get("parkCode"):
        headers["parkCode"] = filepath.config.get("parkCode")
    if not headers.get("Authorization"):
        token = util.get_data_from_json_file("road_toll_system_token")
        headers["Authorization"] = 'Bearer ' + token if token else ''
    for query_data in datas:
        if query_data[0]['id'] == 1:
            sec = query_data[1]['ps']
            request_data = query_data[2].get("request_data")
            if request_data:
                request_data.update(test_data if test_data else {})
            else:
                request_data = test_data
            if custom_param_type:
                res = request.request(method=method, url=url,  headers=headers, timeout=timeout, **test_data)
            elif method.lower() == "post":
                res = request.request(method=method, url=url, data=json.dumps(request_data), headers=headers,
                                      timeout=timeout)
            elif method.lower() == "get":
                res = request.request(method=method, url=url, params=request_data, headers=headers,
                                      timeout=timeout)
            else:
                raise Exception(f"路侧收费系统接口测试暂不支持，请求方式为【{method.lower()}】的接口进行测试！")
            return res
