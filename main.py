# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例
import random
import time

from faker import Faker

f = Faker(locale='zh_CN')
pp = f.bs()
print(pp)
print(pp[0:11])
# print(f.password(length=10,special_chars=False))
# print(f.pystr(min_chars=None, max_chars=5))
#
# def te(length=10,special_chars=True, digits=False, upper_case=False, lower_case=False):
#     f = Faker(locale='zh_CN')
#     print(f.password(length, special_chars, digits, upper_case, lower_case))
# #
# #
# te(length=4)

# print(random.randint(101,103))

print(time.time())