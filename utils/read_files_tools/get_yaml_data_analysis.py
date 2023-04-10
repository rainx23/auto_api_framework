#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/4/1
# @Author : Rainx
"""

import os
from typing import Text, List, Union
from utils.other_tools.models import TestCaseEnum, TestCase
from utils.read_files_tools.yaml_control import GetYamlData
from config.setting import ensure_path_sep
from utils.other_tools.models import Method, RequestType
from utils.cache_process.cache_control import CacheHandler


class CaseDataCheck:
    """ 用例数据校验 """
    def __init__(self, file_path):
        self.file_path = ensure_path_sep(file_path)
        # self.file_path = file_path
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

    def _assert(self, attr: Text):
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    def check_params_exit(self):
        for enum in list(TestCaseEnum._value2member_map_.keys()):
            if enum[1]:
                self._assert(enum[0])

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
    def get_dependence_case_data(self):
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        if _dep_data:
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

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

    def get_yaml_data(self, case_id_switch: Union[None, bool] = None):
        yaml_data = GetYamlData(self.file_path).get_yaml_data()
        case_list = []
        for key, values in yaml_data.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key != 'case_common':
                self.case_data = values
                self.case_id = key
                # super().check_params_exit()
                case_date = {
                    'url': self.get_host,
                    'method': self.get_method,
                    "detail": self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),
                    'requestType': self.get_request_type,
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                    'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),
                    'dependence_case_data': self.get_dependence_case_data,
                    "assert_data": self.assert_data,
                }
                if case_id_switch is True:
                    case_list.append({key: TestCase(**case_date).dict()})
                else:
                    case_list.append(TestCase(**case_date).dict())

        return case_list


class GetTestCase:

    @staticmethod
    def case_data(case_id_lists: List):
        case_lists = []
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_lists.append(_data)

        return case_lists


if __name__ == '__main__':
    c = CaseData('\\data\\UserManger\\update_user_info.yaml').get_yaml_data()
    print(c)
