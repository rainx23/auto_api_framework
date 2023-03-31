# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例

import allure
import pytest

from utils.get_logger import GetLogger
from utils.get_time import GetTime
from api.daxue import DaXue
from utils.get_yml_data import GetYmlData
from utils.requests_tool.request_control import RequestControl
from utils.models import TestCase, RequestType
from utils.assertion.assert_control import Assert
from utils.regular_control import regular


TestData = GetYmlData().get_yml_data('data/test.yml')
re_data = regular(str(TestData))


class TestCaseDaXue:
    time = GetTime().get_now_datetime()
    logger = GetLogger().get_logger()

    def setup(self):
        self.logger.info(self.time + " >>>>>> 开始执行：")

    def teardown(self):
        self.logger.info(self.time + " >>>>>> 执行结束！")

    @pytest.mark.parametrize("data", eval(re_data), ids=[i['title'] for i in TestData])
    def test_query(self, data):

        allure.dynamic.title(data['title'])
        print(data)
        print("@@@@@@@")
        res = RequestControl(data).http_request()
        print(Assert(assert_data=data['assert_data'],
             request_data=res.body,
             response_data=res.response_data,
             status_code=res.status_code).assert_type_handle())


if __name__ == '__main__':
    pytest.main()
