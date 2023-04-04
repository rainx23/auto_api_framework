# -*- coding:utf-8 -*-
"""
# 作者：Rainx
# 时间：2023/3/28
# 功能：封装request请求
"""

import requests
from utils.other_tools.models import TestCase, ResponseData, RequestType
from typing import Dict, Text
from utils.allure_data.allure_tools import allure_step, allure_step_no
from utils.logging_tools.log_decorator import log_decorator


class RequestControl:
    """ 封装请求 """

    def __init__(self, yaml_case):
        self.__yaml_case = TestCase(**yaml_case)

    @classmethod
    def check_headers_str_null(
            cls,
            headers: Dict) -> Dict:
        """
        兼容用户未填写headers或者header值为int
        @return:
        """
        if headers is None:
            headers = {"headers": None}
        else:
            for key, value in headers.items():
                if not isinstance(value, str):
                    headers[key] = str(value)
        return headers

    @classmethod
    def response_elapsed_total_seconds(
            cls,
            res) -> float:
        """获取接口响应时长"""
        try:
            return round(res.elapsed.total_seconds() * 1000, 2)
        except AttributeError:
            return 0.00

    def request_type_for_json(
            self,
            headers: Dict,
            method: Text,
            **kwargs):
        """ 判断请求类型为json格式 """
        _headers = self.__yaml_case.headers
        _data = self.__yaml_case.data
        _url = self.__yaml_case.url
        res = requests.request(
            method=method,
            url=_url,
            json=_data,
            data={},
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_none(
            self,
            headers: Dict,
            method: Text,
            **kwargs) -> object:
        """判断 requestType 为 None"""
        _headers = self.__yaml_case.headers
        _url = self.__yaml_case.url
        res = requests.request(
            method=method,
            url=_url,
            data=None,
            headers=_headers,
            verify=False,
            params=None,
            **kwargs
        )
        return res

    def request_type_for_params(
            self,
            headers: Dict,
            method: Text,
            **kwargs):

        """处理 requestType 为 params """
        _data = self.__yaml_case.data
        url = self.__yaml_case.url
        if _data is not None:
            # url 拼接的方式传参
            params_data = "?"
            for key, value in _data.items():
                if value is None or value == '':
                    params_data += (key + "&")
                else:
                    params_data += (key + "=" + str(value) + "&")
            url = self.__yaml_case.url + params_data[:-1]
        _headers = self.check_headers_str_null(headers)
        res = requests.request(
            method=method,
            url=url,
            headers=_headers,
            verify=False,
            data={},
            params=None,
            **kwargs)
        return res
        pass

    def request_type_for_file(
            self,
            method: Text,
            headers,
            **kwargs):
        """处理 requestType 为 file 类型"""
        # multipart = self.upload_file()
        # yaml_data = multipart[2]
        # _headers = multipart[2].headers
        # _headers = self.check_headers_str_null(_headers)
        # res = requests.request(
        #     method=method,
        #     url=cache_regular(yaml_data.url),
        #     data=multipart[0],
        #     params=multipart[1],
        #     headers=ast.literal_eval(cache_regular(str(_headers))),
        #     verify=False,
        #     **kwargs
        # )
        # return res
        pass

    def request_type_for_data(
            self,
            headers: Dict,
            method: Text,
            **kwargs):
        """判断 requestType 为 data 类型"""
        data = self.__yaml_case.data
        # _data, _headers = self.multipart_in_headers(
        #     ast.literal_eval(cache_regular(str(data))),
        #     headers
        # )
        _url = self.__yaml_case.url
        res = requests.request(
            method=method,
            url=_url,
            data=data,
            headers=headers,
            verify=False,
            **kwargs)

        return res

    def request_type_for_export(self):
        pass

    def _check_params(
            self,
            res,
            yaml_data: "TestCase",
    ) -> "ResponseData":
        _data = {
            "url": res.url,
            "is_run": None,
            "detail": yaml_data.detail,
            "response_data": res.json(),
            # 这个用于日志专用，判断如果是get请求，直接打印url
            "request_body": None,
            "method": res.request.method,
            "sql_data": None,
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "assert_data": yaml_data.assert_data,
            "res_time": self.response_elapsed_total_seconds(res),
            "status_code": res.status_code,
            "teardown": None,
            "teardown_sql": None,
            "body": None
        }
        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**_data)

    @classmethod
    def api_allure_step(
            cls,
            *,
            url: Text,
            headers: Text,
            method: Text,
            data: Text,
            assert_data: Text,
            res_time: Text,
            res: Text
    ) -> None:
        """ 在allure中记录请求数据 """
        allure_step_no(f"请求URL: {url}")
        allure_step_no(f"请求方式: {method}")
        allure_step("请求头: ", headers)
        allure_step("请求数据: ", data)
        allure_step("预期数据: ", assert_data)
        _res_time = res_time
        allure_step_no(f"响应耗时(ms): {str(_res_time)}")
        allure_step("响应结果: ", res)

    @log_decorator(True)
    def http_request(self, **kwargs):

        requests_type_mapping = {
            RequestType.JSON.value: self.request_type_for_json,
            RequestType.NONE.value: self.request_type_for_none,
            RequestType.PARAMS.value: self.request_type_for_params,
            RequestType.FILE.value: self.request_type_for_file,
            RequestType.DATA.value: self.request_type_for_data,
            RequestType.EXPORT.value: self.request_type_for_export
        }

        res = requests_type_mapping.get(self.__yaml_case.requestType)(
            headers=self.__yaml_case.headers,
            method=self.__yaml_case.method,
            **kwargs
        )

        _res_data = self._check_params(
            res=res,
            yaml_data=self.__yaml_case)

        self.api_allure_step(
            url=_res_data.url,
            headers=str(_res_data.headers),
            method=_res_data.method,
            data=str(_res_data.body),
            assert_data=str(_res_data.assert_data),
            res_time=str(_res_data.res_time),
            res=_res_data.response_data
        )

        return _res_data
