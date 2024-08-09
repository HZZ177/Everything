#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 17:33
# @Author  : Heshouyi
# @File    : admin_swagger.py
# @Software: PyCharm
# @description:
import os
import json
import re
import requests
from findcar_auto.common.config_loader import configger


class App:

    def __init__(self, service):
        # 从环境变量中获取环境类型，默认为开发环境
        self.env = os.getenv('ENV', 'dev')       # dev 开发环境/ temp 临时环境
        self.service = service  # 服务名称
        self.config = configger.load_config()

        # 基本参数
        self.base_url = self.config['url'][self.service + '_url']
        self.swagger_url = self.base_url + self.config['swagger_path'][self.service]
        self.swagger_data = None
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(self.current_path, 'data')
        self.json_file_path = os.path.join(self.data_path, f'{self.service}_swagger_data.json')
        self.function_file_path = os.path.join(self.data_path, f'{self.service}_generated_functions.py')

        # 确保目录存在
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # swagger到python的数据类型映射
        self.type_mapping = {
            'integer': 'int',
            'string': 'str',
            'boolean': 'bool',
            'array': 'list',
            'object': 'dict'
        }

    def get_json_data(self):
        try:
            # HTTP请求获取Swagger文档，并格式化
            response = requests.get(self.swagger_url)
            response.raise_for_status()
            self.swagger_data = response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            exit(1)
        except json.JSONDecodeError as e:
            print(f"解析JSON失败: {e}")
            exit(1)

        # 保存json到文件，ensure_ascii=False表示不自动转ASCII码
        with open(f'{self.json_file_path}', 'w', encoding='utf-8') as f:
            json.dump(self.swagger_data, f, ensure_ascii=False, indent=2)

    def create_request_function(self, path, method, operation, custom_function_name=None):
        # 使用自定义函数名或自动生成的函数名
        if custom_function_name:
            function_name = custom_function_name
        else:
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 2:
                function_name = f"{str(path_parts[-2]).replace('-', '')}_{str(path_parts[-1]).replace('-', '_')}".lower()
            else:
                function_name = path_parts[-1].lower()

        summary = operation.get('summary', '暂无参数描述').replace('\n', ' ')
        params = operation.get('parameters', [])

        # 动态生成函数代码
        param_names = []
        param_list = []
        param_annotations = []
        query_params = []
        path_params = []
        body_params = {}

        for param in params:
            param_name = param['name']
            if param['in'] == 'query':
                query_params.append(param_name)
                param_list.append(f"{param_name}: {self.type_mapping.get(param.get('type', 'string'), 'str')}")
                param_names.append(param_name)
                param_annotations.append(
                    f":param {self.type_mapping.get(param.get('type', 'string'), 'str')} {param_name}: {param.get('description', '暂无参数描述')}")
            elif param['in'] == 'path':
                path_params.append(param_name)
                param_list.append(f"{param_name}: {self.type_mapping.get(param.get('type', 'string'), 'str')}")
                param_names.append(param_name)
                param_annotations.append(
                    f":param {self.type_mapping.get(param.get('type', 'string'), 'str')} {param_name}: {param.get('description', '暂无参数描述')}")
            elif param['in'] == 'body' and '$ref' in param['schema']:
                ref = param['schema']['$ref'].split('/')[-1]
                definition = self.swagger_data['definitions'][ref]
                for prop, prop_details in definition['properties'].items():
                    prop_name = prop
                    prop_type = self.type_mapping.get(prop_details.get('type', 'string'), 'str')
                    body_params[prop_name] = prop_type
                    param_list.append(f"{prop_name}: {prop_type}")
                    param_names.append(prop_name)
                    param_annotations.append(
                        f":param {prop_type} {prop_name}: {prop_details.get('description', '暂无参数描述')}")
            else:
                param_type = self.type_mapping.get(param.get('type', 'string'), 'str')
                param_list.append(f"{param_name}: {param_type}")
                param_names.append(param_name)
                param_annotations.append(
                    f":param {param_type} {param_name}: {param.get('description', '暂无参数描述')}")

        param_list.append("token=''")
        param_names.append("token")
        param_annotations.append(":param token: 接口请求Token")

        param_str = ", ".join(param_list)
        param_annotations_str = "\n    ".join(param_annotations)
        function_code = f"def {function_name}({param_str}):\n"
        function_code += f'    """\n    {summary}\n    {param_annotations_str}\n    """\n'
        function_code += f"    url = config['url']['{self.service}_url'] + '{path}'\n"

        # 构建请求头
        function_code += "    headers = {\n"
        function_code += "        'Accesstoken': f'{token}'\n"
        function_code += "    }\n"

        # 处理 path 参数
        for param_name in path_params:
            function_code += f"    url = url.replace('{{{param_name}}}', str({param_name}))\n"

        # 构建请求参数字典 (仅在GET请求中使用)
        if method.upper() == 'GET':
            function_code += "    params = {\n"
            for param_name in query_params:
                function_code += f"        '{param_name}': {param_name},\n"
            function_code += "    }\n"

        # 添加发送请求的固定代码
        if method.upper() == 'POST':
            function_code += "    data = {\n"
            for param_name in param_names:
                if param_name not in path_params and param_name != 'token':
                    function_code += f"        '{param_name}': {param_name},\n"
            function_code += "    }\n"
            function_code += f"    res = requests.request('{method.upper()}', url, json=data, headers=headers)\n"
        elif method.upper() == 'GET':
            function_code += f"    res = requests.request('{method.upper()}', url, params=params, headers=headers)\n"
        else:
            function_code += f"    raise ValueError('Unsupported method: {method}')\n"

        function_code += "    try:\n"
        function_code += "        message = res.json()\n"
        function_code += "        if message['message'] != '成功':\n"
        function_code += "            logger.info(f'接口返回失败，接口返回message：{message['message']}')\n"
        function_code += "        else:\n"
        function_code += "            logger.info(f'接口返回成功！')\n"
        function_code += "        return message\n"
        function_code += "    except Exception:\n"
        function_code += "        logger.exception(f'接口返回信息格式化失败，请求结果：{res}，报错信息：')\n"
        function_code += "\n\n"

        return function_code

    def generate_functions_for_paths(self, paths, custom_function_names=None):
        if custom_function_names is None:
            custom_function_names = {}

        functions_code = ""

        for path in paths:
            path_item = self.swagger_data['paths'].get(path)
            if not path_item:
                raise ValueError(f"路径不存在: {path}")

            for method, operation in path_item.items():
                custom_function_name = custom_function_names.get(path)
                function_code = self.create_request_function(path, method, operation, custom_function_name)
                functions_code += function_code

        return functions_code

    def generate_all_functions(self):
        paths = list(self.swagger_data['paths'].keys())
        return self.generate_functions_for_paths(paths)

    def generate(self, functions_code):
        # 将生成的函数代码保存到文件
        with open(f'{self.function_file_path}', 'w', encoding='utf-8') as f:
            f.write("import requests\n")
            f.write("from findcar_auto.common.config_loader import configger\n")
            f.write("from findcar_auto.common.log_tool import logger\n\n")
            f.write("config = configger.load_config()\n\n\n")
            f.write(functions_code)
            f.write("if __name__ == '__main__':\n")
            f.write("    pass\n")


if __name__ == '__main__':

    app = App('admin')
    app.get_json_data()

    # 生成多个路径的请求函数
    paths = [
        '/lot-info/update',
        '/lot-info/lotInfoCheck'
    ]  # 接口的实际路由列表
    # 自定义函数名对应关系，不传的默认用地址拼接作为函数名
    custom_function_names = {
        '/lot-info/update': 'save_lotinfos',
        '/lot-info/lotInfoCheck': 'check_lotinfo'
    }

    functions_code = app.generate_functions_for_paths(paths, custom_function_names)
    app.generate(functions_code)
    # res = app.generate_all_functions()
    # app.generate(res)
