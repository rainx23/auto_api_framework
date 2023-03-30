# -*- coding:utf-8 -*-
import types
from enum import Enum, unique
from typing import Text, Dict, Callable, Union, Optional, List, Any
from dataclasses import dataclass
from pydantic import BaseModel, Field


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
    URL = ("url", True)
    HOST = ("host", True)
    METHOD = ("method", True)
    TITLE = ("title", True)
    HEADERS = ("headers", True)
    CONTENT_TYPE = ("content_type", True)
    REQUEST_TYPE = ("requestType", True)
    DATA = ("data", True)
    ASSERT_DATA = ("assert_data", True)


class TestCase(BaseModel):
    url: Text
    method: Text
    headers: Union[None, Dict, Text] = {}
    content_type: Text
    requestType: Text
    title: Text
    data: Union[None, Dict, Text] = {}
    assert_data: Union[Dict, Text]


class ResponseData(BaseModel):
    url: Text
    is_run: Union[None, bool, Text]
    detail: None
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
    host: Text

