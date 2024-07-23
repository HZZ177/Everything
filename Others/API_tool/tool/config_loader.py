#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/23 14:03
# @Author  : Heshouyi
# @File    : config_loader.py
# @Software: PyCharm
# @description:
import yaml
import os


class ConfigLoader:
    def __init__(self, env='dev'):
        config_file = os.path.join(os.path.dirname(__file__), f"../config_{env}.yml")
        self.config = self._load_config(config_file)

    @staticmethod
    def _load_config(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {file_path} 未找到")
        except yaml.YAMLError:
            raise ValueError(f"解析配置文件 {file_path} 失败")