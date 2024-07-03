#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 17:33
# @Author  : Heshouyi
# @File    : channel_swagger.py
# @Software: PyCharm
# @description:

import requests
import json

# 固定base_url
base_url = 'http://119.3.77.222:35022'
# 拼接Swagger文档URL
swagger_url = base_url + '/v2/api-docs?group=front-api'

# HTTP请求获取Swagger文档，并格式化
response = requests.get(swagger_url)
swagger_data = response.json()


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
    functions_code = ""

    # 提取接口路径和方法
    for path, path_item in swagger_data['paths'].items():
        for method, operation in path_item.items():
            # 使用路径的倒数第二部分和倒数第一部分组合作为函数名，并转换为小写，路径有-的直接去掉
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 2:
                function_name = f"{str(path_parts[-2]).replace("-", "")}_{path_parts[-1]}".lower()
            else:
                function_name = path_parts[-1].lower()

            summary = operation.get('summary', 'No summary provided').replace('\n', ' ')

            params = operation.get('parameters', [])

            # 动态生成函数代码
            param_names = []
            param_list = []
            param_annotations = []

            for param in params:
                if param['in'] == 'body' and '$ref' in param['schema']:
                    ref = param['schema']['$ref'].split('/')[-1]
                    definition = swagger_data['definitions'][ref]
                    for prop, prop_details in definition['properties'].items():
                        prop_type = type_mapping.get(prop_details.get('type', 'string'), 'str')
                        param_names.append(prop.lower())
                        param_list.append(f"{prop.lower()}: {prop_type}")
                        param_annotations.append(f":param {prop_type} {prop.lower()}: {prop_details.get('description', 'No description')}")
                else:
                    param_type = type_mapping.get(param.get('type', 'string'), 'str')
                    param_names.append(param['name'].lower())
                    param_list.append(f"{param['name'].lower()}: {param_type}")
                    param_annotations.append(f":param {param_type} {param['name'].lower()}: {param.get('description', 'No description')}")

            param_str = ", ".join(param_list)
            param_annotations_str = "\n    ".join(param_annotations)
            function_code = f"def {function_name}({param_str}):\n"
            function_code += f'    """\n    {summary}\n    {param_annotations_str}\n    """\n'
            function_code += f"    url = '{base_url}' + '{path}'\n"

            # 构建请求参数字典
            function_code += "    params = {\n"
            for param_name in param_names:
                function_code += f"        '{param_name}': {param_name},\n"
            function_code += "    }\n"

            # 添加发送请求的代码
            function_code += "    response = requests.request('{}', url, json=params)\n".format(method.upper())
            function_code += "    return response.json()\n"
            function_code += "\n\n"

            functions_code += function_code

    return functions_code


# 动态生成的请求函数代码
request_functions_code = create_request_functions(swagger_data, base_url)

# 将生成的函数代码保存到文件
with open('generated_request_functions.py', 'w', encoding='utf-8') as f:
    f.write("import requests\n\n#############################\n\n\n")
    f.write(request_functions_code)
