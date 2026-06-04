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
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    # 手动清空 report 目录。这个 fixture 默认没有自动执行，需要在用例里主动使用。
    del_file(ensure_path_sep("\\report"))


@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    获取登录的token
    :return:
    """

    # autouse=True 表示测试会话开始时自动执行一次。
    # 这里先调用登录接口，把返回的 token 放到内存缓存里。
    # 后续 yaml 里的 $cache{token} 会被替换成这个 token。
    url = "http://127.0.0.1:8888/api/private/v1/login"
    data = {
        "username": "admin",
        "password": "123456"
    }
    headers = {'Content-Type': 'application/json'}
    # 请求登录接口

    res = requests.post(url=url, data=json.dumps(data), verify=True, headers=headers).json()
    token = res['data']['token']

    # token 只在本次 pytest 进程内有效，不会写入磁盘文件。
    CacheHandler.update_cache(cache_name='token', value=token)
