#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 17:33
# @Author  : Heshouyi
# @File    : admin_swagger.py
# @Software: PyCharm
# @description:
import re
import requests
import json


# 外网base_url，用的时候需要走运维中心把7072代理出来
# base_url = 'http://119.3.77.222:35022'

# 内网固定base_url
base_url = 'http://192.168.21.249:7072'
# 拼接Swagger文档URL
swagger_url = base_url + '/v2/api-docs?group=front-api'

# HTTP请求获取Swagger文档，并格式化
try:
    response = requests.get(swagger_url)
    response.raise_for_status()  # 检查是否请求成功
    swagger_data = response.json()
except requests.RequestException as e:
    print(f"请求失败: {e}")
    exit()
except ValueError as e:
    print(f"解析JSON失败: {e}")
    exit()


# 保存json到文件，ensure_ascii=False表示不自动转ASCII码
with open('channel_swagger_data.json', 'w', encoding='utf-8') as f:
    json.dump(swagger_data, f, ensure_ascii=False, indent=2)


# swagger到python的数据类型映射
type_mapping = {
    'integer': 'int',
    'string': 'str',
    'boolean': 'bool',
    'array': 'list',
    'object': 'dict'
}


# 动态生成请求函数
def create_request_functions(swagger_data, base_url):
    functions_code = "class ChannelAPI:\n"
    functions_code += "    def __init__(self, base_url):\n"
    functions_code += "        self.base_url = base_url\n\n"

    # 提取接口路径和方法
    for path, path_item in swagger_data['paths'].items():
        # 跳过包含 **、{xxx} 和中文字符的路径
        if '**' in path or '{' in path or re.search('[\u4e00-\u9fff]', path):
            continue

        for method, operation in path_item.items():
            # 使用路径的倒数第二部分和倒数第一部分组合作为函数名，并转换为小写，路径有-的直接去掉
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 2:
                function_name = f"{str(path_parts[-2]).replace('-', '')}_{str(path_parts[-1]).replace('-', '_')}".lower()
            else:
                function_name = path_parts[-1].lower()

            summary = operation.get('summary', 'No summary provided').replace('\n', ' ')

            params = operation.get('parameters', [])

            # 动态生成函数代码
            param_names = []
            param_list = []
            default_param_list = []
            param_annotations = []
            query_params = []
            path_params = []
            body_params = {}

            for param in params:
                param_name = param['name'].lower()
                if param['in'] == 'query':
                    query_params.append(param_name)
                elif param['in'] == 'path':
                    path_params.append(param_name)
                elif param['in'] == 'body' and '$ref' in param['schema']:
                    ref = param['schema']['$ref'].split('/')[-1]
                    definition = swagger_data['definitions'][ref]
                    for prop, prop_details in definition['properties'].items():
                        prop_name = prop.lower()
                        prop_type = type_mapping.get(prop_details.get('type', 'string'), 'str')
                        body_params[prop_name] = prop_type
                        default_value = prop_details.get('example', '')
                        if default_value is not None:
                            default_param_list.append(f"{prop_name}: {prop_type} = {repr(default_value)}")
                        else:
                            param_list.append(f"{prop_name}: {prop_type} = ''")
                        param_names.append(prop_name)
                        param_annotations.append(f":param {prop_type} {prop_name}: {prop_details.get('description', 'No description')}")
                else:
                    param_type = type_mapping.get(param.get('type', 'string'), 'str')
                    default_value = param.get('example', '')
                    if default_value is not None:
                        default_param_list.append(f"{param_name}: {param_type} = {repr(default_value)}")
                    else:
                        param_list.append(f"{param_name}: {param_type} = ''")
                    param_names.append(param_name)
                    param_annotations.append(f":param {param_type} {param_name}: {param.get('description', 'No description')}")

            param_list.append("access_token: str")
            param_names.append("access_token")
            param_annotations.append(":param str access_token: The access token for authentication")

            all_param_list = param_list + default_param_list
            param_str = ", ".join(all_param_list)
            param_annotations_str = "\n    ".join(param_annotations)
            function_code = f"    def {function_name}(self, {param_str}):\n"
            function_code += f'        """\n        {summary}\n        {param_annotations_str}\n        """\n'
            function_code += f"        url = self.base_url + '{path}'\n"

            # 构建请求参数字典
            function_code += "        params = {\n"
            for param_name in param_names:
                if param_name != 'access_token':
                    function_code += f"            '{param_name}': {param_name},\n"
            function_code += "        }\n"

            # 构建请求头
            function_code += "        headers = {\n"
            function_code += "            'Accesstoken': f'{access_token}'\n"
            function_code += "        }\n"

            # 添加发送请求的代码
            function_code += f"        response = requests.request('{method.upper()}', url, json=params, headers=headers)\n"
            function_code += "        return response.json()\n"
            function_code += "\n\n"

            functions_code += function_code

    return functions_code

# 动态生成的请求函数代码
request_functions_code = create_request_functions(swagger_data, base_url)

# 将生成的函数代码保存到文件
with open('generated_request_functions.py', 'w', encoding='utf-8') as f:
    f.write("import requests\n\n\n")
    f.write(request_functions_code)
