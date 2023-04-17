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

str = input().split(" ")
print(str)
output = ''
for i in str[::-1]:
    output += (i + ' ')
print(output)
print(output[:-1])