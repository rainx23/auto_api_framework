#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/4/2
# @Author : Rainx
"""
断言类型封装，支持json响应断言、数据库断言
"""
import ast
import json
from typing import Text, Dict, Any, Union
from jsonpath import jsonpath
from utils.other_tools.models import AssertMethod
from utils.other_tools.models import load_module_functions
from utils.logging_tools.log_control import ERROR, WARNING
from utils.read_files_tools.regular_control import cache_regular
from utils.assertion import assert_type
from utils.other_tools.exceptions import JsonpathExtractionFailed, SqlNotFound, AssertTypeError
from utils import config


class AssertUtil:

    def __init__(self, assert_data, request_data, response_data, status_code):
        # assert_data 来自 yaml 的 assert 字段。
        # response_data 是接口返回值，request_data 是本次接口请求体。
        self.response_data = response_data
        self.assert_data = assert_data
        self.request_data = request_data
        self.status_code = status_code

    @property
    def get_assert_data(self):
        assert self.assert_data is not None, (
                "'%s' should either include a `assert_data` attribute, "
                % self.__class__.__name__
        )
        return self.assert_data

    @property
    def get_value(self):
        assert 'value' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `value` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("value")

    @property
    def get_jsonpath(self):
        assert 'jsonpath' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `jsonpath` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("jsonpath")

    @property
    def get_assert_type(self):
        assert 'AssertType' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `AssertType` 属性 " % self.get_assert_data
        )
        return self.get_assert_data.get("AssertType")

    @property
    def get_type(self):
        assert 'type' in self.get_assert_data.keys(), (
            " 断言数据: '%s' 中缺少 `type` 属性 " % self.get_assert_data
        )

        # 获取断言类型对应的枚举值
        name = AssertMethod(self.get_assert_data.get("type")).name
        return name

    @property
    def get_message(self):
        """
        获取断言描述，如果未填写，则返回 `None`
        :return:
        """
        return self.get_assert_data.get("message", None)

    @staticmethod
    def functions_mapping():

        return load_module_functions(assert_type)

    def _assert(self, check_value: Any, expect_value: Any, message: Text = ""):

        # 根据 yaml 中的 type 字段选择具体断言函数，例如 ==、contains、len_eq。
        self.functions_mapping()[self.get_type](check_value, expect_value, str(message))

    @property
    def _assert_resp_data(self):
        # 用 jsonpath 从接口响应中取实际值，例如 $.meta.status。
        resp_data = jsonpath(self.response_data, self.get_jsonpath)
        assert resp_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.response_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(resp_data) > 1:
            return resp_data
        return resp_data[0]

    @property
    def _assert_request_data(self):
        # 预留能力：也可以用 jsonpath 从请求参数中取值做断言。
        req_data = jsonpath(self.request_data, self.get_jsonpath)
        assert req_data is not False, (
            f"jsonpath数据提取失败，提取对象: {self.request_data} , 当前语法: {self.get_jsonpath}"
        )
        if len(req_data) > 1:
            return req_data
        return req_data[0]

    def assert_type_handle(self):
        if self.get_assert_type is None:
            self._assert(self._assert_resp_data, self.get_value, self.get_message)

        else:
            raise AssertTypeError("断言失败，目前只支持数据库断言和响应断言")


class Assert(AssertUtil):

    def assert_data_list(self):
        # yaml 的 assert 下面可以配置多个断言项，这里统一整理成列表逐个执行。
        assert_list = []

        for k, v in self.assert_data.items():
            if k == "status_code":
                assert self.status_code == v, "响应状态码断言失败"
            else:
                assert_list.append(v)

        return assert_list

    def assert_type_handle(self):
        # 遍历每一条断言配置，只要有一条失败，pytest 就会判定该用例失败。
        for i in self.assert_data_list():

            self.assert_data = i
            super().assert_type_handle()

