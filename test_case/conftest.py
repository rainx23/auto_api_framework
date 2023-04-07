#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/4/7
# @Author : Rainx
import pytest
import json
import allure
import requests
import ast
from config.setting import ensure_path_sep
from utils.logging_tools.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tools.clean_files import del_file
from utils.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    del_file(ensure_path_sep("\\report"))


@pytest.fixture(scope="session", autouse=False)
def work_login_init():
    """
    获取登录的token
    :return:
    """

    url = "http://127.0.0.1:8888/api/private/v1/login"
    data = {
        "username": "admin",
        "password": "123456"
    }
    headers = {'Content-Type': 'application/json'}
    # 请求登录接口

    res = requests.post(url=url, data=json.dumps(data), verify=True, headers=headers).json()
    token = res['data']['token']

    CacheHandler.update_cache(cache_name='Authorization', value=token)

