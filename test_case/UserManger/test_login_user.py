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


# 读取登录接口的 yaml 用例数据。
TestData = CaseData("\\data\\UserManger\\login_user.yaml").get_yaml_data()
# 把 yaml 里的动态表达式替换成真实值，例如 ${{host()}}、${{get_username()}}。
re_data = regular(str(TestData))


@allure.epic("商城平台接口")
@allure.feature("用户管理")
class TestLoginUser:

    @allure.story("用户登录")
    # parametrize 会把 yaml 中的多条登录用例拆成多条 pytest 测试。
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_login_user(self, in_data):
        """
        :param :
        :return:
        """
        allure.dynamic.title(in_data['detail'])
        # 发送接口请求，得到统一封装后的响应对象。
        res = RequestControl(in_data).http_request()
        # 如果用例配置了 teardown，这里会执行后置清理。
        TearDownHandler(res).teardown_handle()
        # 根据 yaml 中的 assert 字段校验响应。
        Assert(assert_data=in_data['assert_data'],
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['test_login_user.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
