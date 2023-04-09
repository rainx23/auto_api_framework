# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例

from faker import Faker

# f = Faker(locale='zh_CN')
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
yaml_case = {'url': 'http://127.0.0.1:8888/api/private/v1/users/$url_params{id}', 'method': 'PUT', 'detail': '修改用户信息', 'headers': {'Authorization': '$cache{token}'}, 'is_run': True, 'dependence_case': True, 'dependence_case_data': [{'case_id': 'create_user_03', 'dependent_data': [{'dependent_type': 'response', 'jsonpath': '$.data.id', 'set_cache': None, 'replace_key': '$url_params{id}'}]}], 'requestType': 'NONE', 'data': None, 'assert_data': {'errorStatus': {'jsonpath': '$.meta.status', 'type': '==', 'value': 200, 'AssertType': None}, 'errorInfo': {'jsonpath': '$.meta.msg', 'type': '==', 'value': '更新成功', 'AssertType': None}}}

print(yaml_case['url'])
def pp():
    exec('yaml_case[\'url\'] = \'http://127.0.0.1:8888/api/private/v1/users/938\'')
pp()
print(yaml_case['url'])

# te = {'$url_params{id}': 862, '$.url': 'http://127.0.0.1:8888/api/private/v1/users/862'}
# for key,value in te.items():
#     print(key.split('.'))
#     print("---")
