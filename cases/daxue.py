#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/4/1
# @Author : Rainx
"""

import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.get_logger import GetLogger
from utils.get_time import GetTime
from utils.requests_tool.request_control import RequestControl
from utils.assertion.assert_control import Assert
from utils.regular_control import regular


TestData = CaseData('\\data\\test.yaml').get_yaml_data()
re_data = regular(str(TestData))


class TestCaseDaXue:
    time = GetTime().get_now_datetime()
    logger = GetLogger().get_logger()

    def setup(self):
        self.logger.info(self.time + " >>>>>> 开始执行：")

    def teardown(self):
        self.logger.info(self.time + " >>>>>> 执行结束！")

    @pytest.mark.parametrize("data", eval(re_data), ids=[i['detail'] for i in TestData])
    def test_query(self, data):

        allure.dynamic.title(data['detail'])
        print(TestData)
        res = RequestControl(data).http_request()
        Assert(assert_data=data['assert_data'],
             request_data=res.body,
             response_data=res.response_data,
             status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main()
