#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2023/4/7 11:56
# @Author : Rainx
"""

import os


def del_file(path):
    """ 删除路径下的文件 """
    list_path = os.listdir(path)
    for i in list_path:
        all_path = os.path.join(path, i)
        if os.path.isdir(all_path):
            del_file(all_path)
        else:
            os.remove(all_path)

