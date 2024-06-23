# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
===================================
@FileName: fileService.py
@Description: 
@Author: huangjunhao
@Software: PyCharm
@Version: 1.0
@Update:
@Copyright: 
@time:2023/06/30
===================================
"""
import base64

import allure

from common import util, filepath
from common.configLog import logger
from common.filepath import ROAD_FILE_PATH
from model.road_park.road_app_api import send_road_app_api


class FileService:
    """
    路内停车助手App文件相关接口
    """

    @util.catch_exception
    @util.retry_fun
    @allure.step("通过路内app查询在场车记录")
    def uploadBase64(self, roadCode, parkCode="", file_name='ts01', **kwargs):
        """通过路内app查询在场车记录

        :param parkCode: 车场编码
        :param roadCode: 路段编码
        :param file_name: 上传图片名称
        """
        with open(ROAD_FILE_PATH + f'/{file_name}.jpg', 'rb') as f:
            pics_base64 = base64.b64encode(f.read()).decode()
        test_data = {"data": f'data:image/jpeg;base64,{pics_base64}',
                     "packageName": f'image/app/{parkCode}/{roadCode}'
                     }
        kwargs.update(test_data)
        res = send_road_app_api(filepath.UPLOAD_FILE_BASE64, 2, header_data={}, test_data=kwargs)
        result_dic = res.json()
        if result_dic["code"] == 200 and result_dic["success"]:
            logger.info(f"✔ 上传文件base64成功！")
            return result_dic
        else:
            raise Exception(f"❌  上传文件base64成功失败！错误为【{result_dic}】!")

