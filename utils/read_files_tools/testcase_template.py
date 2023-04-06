#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/4/6
# @Author  : Rainx
# @Email   : 1106262459@qq.com
# @File    : testcase_template
# @describe: 用例模板
"""

import datetime
import os
from utils import config
from utils.read_files_tools.yaml_control import GetYamlData
from config.setting import ensure_path_sep
from utils.other_tools.exceptions import ValueNotFoundError


def write_case(case_path, page):
    """ 写入用例数据 """
    with open(case_path, 'w', encoding="utf-8") as file:
        file.write(page)


def write_testcase_file(*, allure_epic, allure_feature, class_title,
                        func_title, case_path, yaml_path, file_name, allure_story):
    """

        :param allure_story:
        :param file_name: 文件名称
        :param allure_epic: 项目名称
        :param allure_feature: 模块名称
        :param class_title: 类名称
        :param func_title: 函数名称
        :param case_path: case 路径
        :param case_ids: 用例ID
        :return:
        """
    conf_data = GetYamlData(ensure_path_sep("\\config\\config.yaml")).get_yaml_data()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    real_time_update_test_cases = conf_data['real_time_update_test_cases']

    page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
# @Author : {config.tester_name}

import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.other_tools.get_time import GetTime
from utils.requests_tool.request_control import RequestControl
from utils.assertion.assert_control import Assert
from utils.regular_control import regular
from utils.logging_tools.log_control import INFO


TestData = CaseData("{yaml_path}").get_yaml_data()
re_data = regular(str(TestData))


@allure.epic("{allure_epic}")
@allure.feature("{allure_feature}")
class Test{class_title}:
    time = GetTime().get_now_datetime()

    def setup(self):
        INFO.logger.info(self.time + " >>>>>> 开始执行：")

    def teardown(self):
        INFO.logger.info(self.time + " >>>>>> 执行结束！")

    @allure.story("{allure_story}")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_{func_title}(self, in_data):
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
    pytest.main(['{file_name}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
'''
    if real_time_update_test_cases:
        write_case(case_path=case_path, page=page)
    elif real_time_update_test_cases is False:
        if not os.path.exists(case_path):
            write_case(case_path=case_path, page=page)
    else:
        raise ValueNotFoundError("real_time_update_test_cases 配置不正确，只能配置 True 或者 False")

