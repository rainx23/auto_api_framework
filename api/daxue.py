# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14  15:03
# 功能：将http请求封装成Python方法
import requests
from base_api import BaseApi
from utils.get_yml_data import GetYmlData
from utils.models import TestCase


class DaXue(BaseApi):
    def __init__(self, yaml_data):
        super(DaXue, self).__init__()
        self.__yaml_data = TestCase(**yaml_data)

    def daxue(self, data):
        # 接口信息
        # Request URL
        request_url = "/home/daxue/ajax"
        # Request Method
        method = "POST"
        # ContentType
        content_type = "application/x-www-form-urlencoded"
        res = self.api_temp(request_url, method, content_type, data)
        # print(data)
        return res


if __name__ == '__main__':
    data = GetYmlData().get_yml_data('data/test.yml')


