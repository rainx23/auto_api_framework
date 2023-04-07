#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-04-07 09:59:06
# @Author : Rainx

import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.other_tools.get_time import GetTime
from utils.requests_tool.request_control import RequestControl
from utils.assertion.assert_control import Assert
from utils.regular_control import regular
from utils.logging_tools.log_control import INFO


TestData = CaseData("\\data\\Query\\query_college_info.yaml").get_yaml_data()
re_data = regular(str(TestData))


@allure.epic("开发平台接口")
@allure.feature("查询模块")
class TestQueryCollegeInfo:
    time = GetTime().get_now_datetime()

    def setup(self):
        INFO.logger.info(self.time + " >>>>>> 开始执行：")

    def teardown(self):
        INFO.logger.info(self.time + " >>>>>> 执行结束！")

    @allure.story("查询")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_query_college_info(self, in_data):
        """
        :param :
        :return:
        """
        allure.dynamic.title(in_data['detail'])
        res = RequestControl(in_data).http_request()
        Assert(assert_data=in_data['assert_data'],
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['test_query_college_info.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
