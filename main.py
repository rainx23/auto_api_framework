# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例
import random
import time

# from faker import Faker
#
# f = Faker(locale='zh_CN')
# pp = f.bs()
#
# from typing import Text, List, Union
# from utils.other_tools.models import TestCaseEnum, TestCase
#
# t = {'host':"www.hhh.com"}
# print(list(TestCaseEnum._value2member_map_.keys()))
# print(t.get(TestCaseEnum.HOST.value[0]))
import sys


# list1 = [{'id': 'get_all_purview_list_01', 'host': '${{host()}}', 'url': '/api/private/v1/rights/list', 'method': 'GET', 'detail': '获取所有权限列表展示成功', 'headers': "{'Authorization': '$cache{token}'}", 'requestType': 'None', 'is_run': 'TRUE', 'data': 'None', 'dependence_case': 'None', 'dependence_case_data': 'None', 'assert': 'None', 'sql': 'None'}, {'id': 'get_all_purview_list_02', 'host': '${{host()}}', 'url': '/api/private/v1/rights/list', 'method': 'GET', 'detail': '获取所有权限列表展示成功', 'headers': 'Authorization: $cache{token}', 'requestType': 'None', 'is_run': 'TRUE', 'data': 'None', 'dependence_case': 'None', 'dependence_case_data': 'None', 'assert': 'None', 'sql': 'None'}, {'id': 'get_all_purview_list_03', 'host': '${{host()}}', 'url': '/api/private/v1/rights/list', 'method': 'GET', 'detail': '获取所有权限列表展示成功', 'headers': 'Authorization: $cache{token}', 'requestType': 'None', 'is_run': 'TRUE', 'data': 'None', 'dependence_case': 'None', 'dependence_case_data': 'None', 'assert': 'None', 'sql': 'None'}]
# dic = {}
# for i in range(len(list1)):
#     dic[list1[i]['id']] = list1[i]
# print(dic)


def aa(a,b):
    print('a:', a)


a = {'a': '1', 'b': '2'}

print(aa(**a))
