# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例

import pytest
import requests
import allure
from utils.get_logger import GetLogger
from utils.get_time import GetTime
from api.daxue import DaXue
from utils.get_yml_data import GetYmlData
from base_api import BaseApi


class TestCase:
    time = GetTime().get_now_datetime()
    logger = GetLogger().get_logger()

    def setup(self):
        self.logger.info(self.time + " >>>>>> 开始执行：")

    def teardown(self):
        self.logger.info(self.time + " >>>>>> 执行结束！")

    @pytest.mark.parametrize("info", GetYmlData().get_yml_data('data/test.yaml'))
    def test1(self, info):
        print(info)
        allure.dynamic.title(info['req']['title'])
        method = info['req']['method']
        content_type = info['req']['content_type']
        # data = info['req']['datas']
        # print(data)
        url = info['req']['url']
        # BaseApi().api_temp(url, method, content_type, info)
        DaXue().daxue(info)
        # res = requests.post(url=url, headers=header, data=data)


if __name__ == '__main__':
    pytest.main()
