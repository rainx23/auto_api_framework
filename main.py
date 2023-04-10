# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例

from faker import Faker

f = Faker(locale='zh_CN')
# print(f.password(length=10,special_chars=False))
# print(f.pystr(min_chars=None, max_chars=5))
#
# def te(length=10,special_chars=True, digits=True, upper_case=True, lower_case=True):
#     f = Faker(locale='zh_CN')
#     print(f.password(length, special_chars, digits, upper_case, lower_case))
#
#
# te(length=4)


# url = "/api/private/v1/users/$url_param{id}"
# print(url.replace("$url_param{id}", "258"))
# replace_key = '$url_params{id}'
# if "$url_param" in replace_key:
#     print('11')

# _dependent_data = {'$url_params{id}': 835, '$.url': 'http://127.0.0.1:8888/api/private/v1/users/835'}
# for key, value in _dependent_data.items():
#     print(key)
#     print(value)


# _url = '/api/private/v1/users11'
# _data = {'pagenum':'1','pagesize':'20'}
# if _data is not None:
#     # url 拼接的方式传参
#     params_data = "?"
#     for key, value in _data.items():
#         if value is None or value == '':
#             params_data += (key + "&")
#         else:
#             params_data += (key + "=" + str(value) + "&")
#         print(params_data)
#     url = _url + params_data[:-1]
#     print(url)
#
#
# print(_url[1:-1])

# a = f.unix_time()
# print(a)

import time

a = time.time()
print(int(a))