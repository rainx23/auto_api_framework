#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023-04-13 11:15:25
# @Author : Rainx

import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.requests_tool.request_control import RequestControl
from utils.assertion.assert_control import Assert
from utils.read_files_tools.regular_control import regular


TestData = CaseData("\\data\\ProductManger\\query_product_specified_id.yaml").get_yaml_data()
re_data = regular(str(TestData))


@allure.epic("商城平台接口")
@allure.feature("商品管理")
class TestQueryProductSpecifiedId:

    @allure.story("查询指定ID的商品")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_query_product_specified_id(self, in_data):
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
    pytest.main(['test_query_product_specified_id.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
