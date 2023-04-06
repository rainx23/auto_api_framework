# -*- coding:utf-8 -*-
import types
from enum import Enum, unique
from typing import Text, Dict, Callable, Union, Optional, List, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field


class Method(Enum):
    """ 请求方法数据类型 """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTION = "OPTION"


class RequestType(Enum):
    """
    request请求发送，请求参数的数据类型
    """
    JSON = "JSON"
    PARAMS = "PARAMS"
    DATA = "DATA"
    FILE = 'FILE'
    EXPORT = "EXPORT"
    NONE = "NONE"


class TestCaseEnum(Enum):
    """
    用例字段校验
    """
    HOST = ("host", True)
    URL = ("url", True)
    METHOD = ("method", True)
    DETAIL = ("detail", True)
    HEADERS = ("headers", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    ASSERT_DATA = ("assert", True)


class TestCase(BaseModel):
    url: Text
    method: Text
    detail: Text
    headers: Union[None, Dict, Text] = {}
    requestType: Text
    data: Union[None, Dict, Text] = {}
    assert_data: Union[Dict, Text]


class ResponseData(BaseModel):
    url: Text
    is_run: Union[None, bool, Text]
    detail: Text
    response_data: Any
    request_body: None
    method: Text
    sql_data: None
    yaml_data: "TestCase"
    headers: Dict
    cookie: Dict
    assert_data: Dict
    res_time: Union[None, int, float]
    status_code: int
    teardown: None
    teardown_sql: Union[None, List]
    body: None


class Config(BaseModel):
    project_name: Text
    env: Text
    tester_name: Text
    host: Text
    real_time_update_test_cases: bool = False

@unique
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"
