#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/1
# @Author  : Rainx
# @Function: 读取路径

import os
from typing import Text


def root_path():
    """ 获取 根路径 """
    # 返回项目根目录，例如 C:\...\auto_api_framework。
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    # 把传入的相对路径统一转换成当前系统可识别的路径分隔符。
    # 这样同一套代码在 Windows 和 Linux 上都能尽量正常找到文件。
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path
