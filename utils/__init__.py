# -*- coding: utf-8 -*-
# @Time   : 2022/4/2
# @Author : Rainx
"""
读取配置文件
"""

from utils.read_files_tools.yaml_control import GetYamlData
from config.setting import ensure_path_sep
from utils.other_tools.models import Config


# 项目启动或测试导入 utils 时，会先读取 config/config.yaml。
# 读取后的字典会转换成 Config 对象，后续可以用 config.host 这种方式访问配置。
_data = GetYamlData(ensure_path_sep("\\config\\config.yaml")).get_yaml_data()
config = Config(**_data)
