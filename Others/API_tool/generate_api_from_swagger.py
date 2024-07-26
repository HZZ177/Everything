#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/3 17:33
# @Author  : Heshouyi
# @File    : admin_swagger.py
# @Software: PyCharm
# @description:
import os
import requests
import json
import re
from tool.config_loader import ConfigLoader


class App:

    def __init__(self):

        # 从环境变量中获取环境类型，默认为开发环境
        self.env = os.getenv('ENV', 'dev')       # dev 开发环境/ temp 临时环境
        self.service = 'channel'     # channel、admin、findcar
        self.config = ConfigLoader(self.env).config

        # 基本参数
        self.base_url = self.config['base_url'] + ':' + self.config['port'][self.service]
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

    # 动态生成请求函数
    def create_request_functions(self):
        format_service = self.service.capitalize()
        functions_code = f"class {format_service}API:\n"
        functions_code += "    def __init__(self, base_url):\n"
        functions_code += "        self.base_url = base_url\n\n"

        # 提取接口路径和方法
        for path, path_item in self.swagger_data['paths'].items():
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
                        definition = self.swagger_data['definitions'][ref]
                        for prop, prop_details in definition['properties'].items():
                            prop_name = prop.lower()
                            prop_type = self.type_mapping.get(prop_details.get('type', 'string'), 'str')
                            body_params[prop_name] = prop_type
                            default_value = prop_details.get('example', '')
                            if default_value is not None:
                                default_param_list.append(f"{prop_name}: {prop_type} = {repr(default_value)}")
                            else:
                                param_list.append(f"{prop_name}: {prop_type} = ''")
                            param_names.append(prop_name)
                            param_annotations.append(f":param {prop_type} {prop_name}: {prop_details.get('description', 'No description')}")
                    else:
                        param_type = self.type_mapping.get(param.get('type', 'string'), 'str')
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
                param_annotations_str = "\n        ".join(param_annotations)
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
                function_code += "\n"

                functions_code += function_code

        return functions_code

    def generate(self):
        # 动态生成的请求函数代码
        request_functions_code = self.create_request_functions()

        # 将生成的函数代码保存到文件
        with open(f'{self.function_file_path}', 'w', encoding='utf-8') as f:
            f.write("import requests\n\n\n")
            f.write(request_functions_code)


if __name__ == '__main__':

    app = App()
    app.get_json_data()
    app.create_request_functions()
    app.generate()
