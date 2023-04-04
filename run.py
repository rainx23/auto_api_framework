# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/3/15 16:40
# 功能：批量执行测试用例，并生成Allure测试报告

import os
import pytest


class Run:
    @staticmethod
    def run_default():
        # 测试用例
        case = "test_case/test_query_college_info.py"

        # allure-json存放路径
        allure_json = "reports/"
        if not os.path.exists(allure_json):
            os.makedirs(allure_json)

        # 定义PyTest运行参数
        param_list = [case, "-s", "-v", "-rA", "--alluredir={}".format(allure_json)]

        # 执行用例，并生成测试报告
        pytest.main(param_list)
        os.system("allure generate {} --clean".format(allure_json))


if __name__ == '__main__':
    Run().run_default()
