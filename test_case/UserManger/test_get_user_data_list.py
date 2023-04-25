#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-04-25 17:05:52
# @Author : Rainx

import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.requests_tool.request_control import RequestControl
from utils.assertion.assert_control import Assert
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


TestData = CaseData("\\data\\UserManger\\get_user_data_list.yaml").get_yaml_data()
re_data = regular(str(TestData))


@allure.epic("商城平台接口")
@allure.feature("用户管理")
class TestGetUserDataList:

    @allure.story("获取用户数据列表")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_get_user_data_list(self, in_data):
        """
        :param :
        :return:
        """
        allure.dynamic.title(in_data['detail'])
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['test_get_user_data_list.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
