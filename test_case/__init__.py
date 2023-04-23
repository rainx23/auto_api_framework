#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2023/4/8
# @Author : Rainx

from config.setting import ensure_path_sep, root_path
from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.read_files_tools.get_all_files_path import get_all_files
from utils.cache_process.cache_control import CacheHandler, _cache_config
from utils import config
from utils.read_files_tools.get_excel_data import ExcelCaseData


def write_case_process():
    """
    获取所有用例，写入用例池中
    :return:
    """

    # 循环拿到所有存放用例的文件路径
    for i in get_all_files(file_path=ensure_path_sep("\\data"), yaml_data_switch=True):
        get_yaml_path = i[len(root_path()):].replace("\\", "\\\\")
        # 循环读取文件中的数据
        if config.case_mode == '1':
            case_process = CaseData(get_yaml_path).get_yaml_data(case_id_switch=True)
        elif config.case_mode == '2':
            case_process = ExcelCaseData(get_yaml_path).get_excel_data(case_id_switch=True)
        if case_process is not None:
            # 转换数据类型
            for case in case_process:
                for k, v in case.items():
                    # 判断 case_id 是否已存在
                    case_id_exit = k in _cache_config.keys()
                    # 如果case_id 不存在，则将用例写入缓存池中
                    if case_id_exit is False:
                        CacheHandler.update_cache(cache_name=k, value=v)
                        # case_data[k] = v
                    # 当 case_id 为 True 存在时，则跑出异常
                    elif case_id_exit is True:
                        raise ValueError(f"case_id: {k} 存在重复项, 请修改case_id\n"
                                         f"文件路径: {i}")


write_case_process()

