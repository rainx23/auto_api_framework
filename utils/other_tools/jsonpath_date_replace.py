#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/4/8
# @Author  : Rainx
# @File    : jsonpath_date_replace
# @describe:
"""


def jsonpath_replace(change_data, key_name, data_switch=None):
    """处理jsonpath数据"""
    _new_data = key_name + ''
    for i in change_data:
        if i == '$':
            pass
        elif data_switch is None and i == "data":
            _new_data += '.data'
        # elif data_switch is None and i == "url":
        #     _new_data += '.url'
        elif i[0] == '[' and i[-1] == ']':
            _new_data += "[" + i[1:-1] + "]"
        else:
            _new_data += '[' + '"' + i + '"' + "]"
    return _new_data


if __name__ == '__main__':
    print(jsonpath_replace(change_data=['$', 'url'], key_name='self.__yaml_case'))
    print(jsonpath_replace(change_data=['$url_params{id}'], key_name='self.__yaml_case'))
