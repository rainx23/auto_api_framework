#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/4/1
# @Author : Rainx
"""

import os
from typing import Text
from utils.other_tools.models import TestCaseEnum, TestCase
from utils.read_files_tools.yaml_control import GetYamlData
from config.setting import ensure_path_sep
from utils.other_tools.models import Method, RequestType


class CaseDataCheck:
    """ 用例数据校验 """
    def __init__(self, file_path):
        self.file_path = ensure_path_sep(file_path)
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError("用例地址未找到")

        self.case_data = None
        self.case_id = None

    def check_params_right(self, enum_name, attr):
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员."
            f"当前用例文件路径：{self.file_path}"
        )
        return attr.upper()

    @property
    def get_method(self) -> Text:
        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_host(self) -> Text:
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    @property
    def get_request_type(self) -> Text:
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    def assert_data(self) -> Text:
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        return _assert_data


class CaseData(CaseDataCheck):

    def get_yaml_data(self):
        yaml_data = GetYamlData(self.file_path).get_yaml_data()
        case_list = []
        for key, values in yaml_data.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key != 'case_common':
                self.case_data = values
                self.case_id = key
                case_date = {
                    'url': self.get_host,
                    'method': self.get_method,
                    "detail": self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'requestType': self.get_request_type,
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                    "assert_data": self.assert_data,
                }
                case_list.append(TestCase(**case_date).dict())

        return case_list


if __name__ == '__main__':
    print(CaseData('\\data\\UserManger\\create_user.yaml').get_yaml_data())
