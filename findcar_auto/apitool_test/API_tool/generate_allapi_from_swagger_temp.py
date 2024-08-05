import os
import requests
import json
import re
from tool.config_loader import ConfigLoader

class App:

    def __init__(self):
        self.env = os.getenv('ENV', 'dev')  # dev 开发环境/ temp 临时环境
        self.service = 'channel'  # channel、admin、findCarApi
        self.config = ConfigLoader(self.env).config

        self.base_url = self.config['base_url'] + ':' + self.config['port'][self.service]
        self.swagger_url = self.base_url + self.config['swagger_path'][self.service]
        self.swagger_data = None
        self.current_path = os.path.abspath(os.path.dirname(__file__))
        self.data_path = os.path.join(self.current_path, 'data')
        self.json_file_path = os.path.join(self.data_path, f'{self.service}_swagger_data.json')
        self.function_file_path = os.path.join(self.data_path, f'{self.service}_generated_functions.py')

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.type_mapping = {
            'integer': 'int',
            'string': 'str',
            'boolean': 'bool',
            'array': 'list',
            'object': 'dict'
        }

    def get_json_data(self):
        try:
            response = requests.get(self.swagger_url)
            response.raise_for_status()
            self.swagger_data = response.json()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            exit(1)
        except json.JSONDecodeError as e:
            print(f"解析JSON失败: {e}")
            exit(1)

        with open(f'{self.json_file_path}', 'w', encoding='utf-8') as f:
            json.dump(self.swagger_data, f, ensure_ascii=False, indent=2)

    def parse_parameters(self, params):
        param_names = []
        param_list = []
        param_annotations = []
        body_params = {}

        for param in params:
            param_name = param['name'].lower()
            if param['in'] in ['query', 'path']:
                param_type = self.type_mapping.get(param.get('type', 'string'), 'str')
                param_list.append(f"{param_name}: {param_type}")
                param_names.append(param_name)
                param_annotations.append(f":param {param_type} {param_name}: {param.get('description', 'No description')}")
            elif param['in'] == 'body':
                schema = param.get('schema', {})
                parsed_body_params = self.parse_schema(schema)
                for key, value in parsed_body_params.items():
                    param_list.append(f"{key}: {value[0]}")
                    param_names.append(key)
                    param_annotations.append(f":param {value[0]} {key}: {param.get('description', 'No description')}")
                body_params.update(parsed_body_params)

        return param_names, param_list, param_annotations, body_params

    def parse_schema(self, schema, parent_key=''):
        params = {}
        if '$ref' in schema:
            ref = schema['$ref'].split('/')[-1]
            definition = self.swagger_data['definitions'][ref]
            properties = definition.get('properties', {})
            required = definition.get('required', [])
            for prop, prop_details in properties.items():
                full_key = f"{parent_key}.{prop}" if parent_key else prop
                if prop_details.get('type') == 'object' or '$ref' in prop_details:
                    nested_params = self.parse_schema(prop_details, full_key)
                    params.update(nested_params)
                else:
                    params[full_key] = (self.type_mapping.get(prop_details.get('type', 'string'), 'str'), prop in required)
        elif 'type' in schema:
            if schema['type'] == 'array':
                items = schema.get('items', {})
                full_key = f"{parent_key}[]" if parent_key else 'items[]'
                if items.get('type') == 'object' or '$ref' in items:
                    nested_params = self.parse_schema(items, full_key)
                    params.update(nested_params)
                else:
                    params[full_key] = (self.type_mapping.get(items.get('type', 'string'), 'str'), False)
            elif schema['type'] == 'object':
                properties = schema.get('properties', {})
                for prop, prop_details in properties.items():
                    full_key = f"{parent_key}.{prop}" if parent_key else prop
                    if prop_details.get('type') == 'object' or '$ref' in prop_details:
                        nested_params = self.parse_schema(prop_details, full_key)
                        params.update(nested_params)
                    else:
                        params[full_key] = (self.type_mapping.get(prop_details.get('type', 'string'), 'str'), False)
        return params

    def create_request_function(self, path, method, operation, custom_function_name=None):
        if custom_function_name:
            function_name = custom_function_name
        else:
            path_parts = path.strip('/').split('/')
            if len(path_parts) >= 2:
                function_name = f"{str(path_parts[-2]).replace('-', '')}_{str(path_parts[-1]).replace('-', '_')}".lower()
            else:
                function_name = path_parts[-1].lower()

        summary = operation.get('summary', 'No summary provided').replace('\n', ' ')
        params = operation.get('parameters', [])

        param_names, param_list, param_annotations, body_params = self.parse_parameters(params)

        param_list.append("access_token: str")
        param_names.append("access_token")
        param_annotations.append(":param str access_token: The access token for authentication")

        param_str = ", ".join(param_list)
        param_annotations_str = "\n        ".join(param_annotations)
        function_code = f"    def {function_name}(self, {param_str}):\n"
        function_code += f'        """\n        {summary}\n        {param_annotations_str}\n        """\n'
        function_code += f"        url = self.base_url + '{path}'\n"

        function_code += "        params = {\n"
        for param in param_names:
            if param != 'access_token':
                function_code += f"            '{param}': {param},\n"
        function_code += "        }\n"

        function_code += "        headers = {\n"
        function_code += "            'Accesstoken': f'{access_token}'\n"
        function_code += "        }\n"

        function_code += f"        response = requests.request('{method.upper()}', url, json=params, headers=headers)\n"
        function_code += "        return response.json()\n"
        function_code += "\n"

        return function_code

    def create_request_functions(self):
        format_service = self.service.capitalize()
        functions_code = f"class {format_service}API:\n"
        functions_code += "    def __init__(self, base_url):\n"
        functions_code += "        self.base_url = base_url\n\n"

        for path, path_item in self.swagger_data['paths'].items():
            if '**' in path or '{' in path or re.search('[\u4e00-\u9fff]', path):
                continue

            for method, operation in path_item.items():
                function_code = self.create_request_function(path, method, operation)
                functions_code += function_code

        return functions_code

    def generate_functions_for_paths(self, paths, custom_function_names=None):
        if custom_function_names is None:
            custom_function_names = {}

        format_service = self.service.capitalize()
        functions_code = f"class {format_service}API:\n"
        functions_code += "    def __init__(self, base_url):\n"
        functions_code += "        self.base_url = base_url\n\n"

        for path in paths:
            path_item = self.swagger_data['paths'].get(path)
            if not path_item:
                raise ValueError(f"No such path: {path}")

            for method, operation in path_item.items():
                custom_function_name = custom_function_names.get(path)
                function_code = self.create_request_function(path, method, operation, custom_function_name)
                functions_code += function_code

        return functions_code

    def generate(self):
        request_functions_code = self.create_request_functions()

        with open(f'{self.function_file_path}', 'w', encoding='utf-8') as f:
            f.write("import requests\n\n\n")
            f.write(request_functions_code)


if __name__ == '__main__':
    app = App()
    app.get_json_data()

    paths = ['/park/enter', '/park/updatePlateNo']  # 替换为实际路径列表
    custom_function_names = {
        '/park/enter': 'custom_function_name1',
        '/park/updatePlateNo': 'custom_function_name2'
    }
    functions_code = app.generate_functions_for_paths(paths, custom_function_names)
    print(functions_code)  # 输出或保存到文件
