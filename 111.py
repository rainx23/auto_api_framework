
# -*- coding:utf-8 -*-
data = [{'url': 'https://www.wanandroid.com/user/lg/userinfo/json', 'method': 'GET', 'detail': '正常获取个人身份信息', 'assert_data': {'errorCode': {'jsonpath': '$.errorCode', 'type': '==', 'value': 0, 'AssertType': None}, 'username': {'jsonpath': '$.data.userInfo.username', 'type': '==', 'value': '18800000001', 'AssertType': None}}, 'headers': {'Content-Type': 'multipart/form-data;', 'cookie': '$cache{login_cookie}'}, 'requestType': 'DATA', 'is_run': None, 'data': None, 'dependence_case': False, 'dependence_case_data': None, 'sql': None, 'setup_sql': None, 'status_code': None, 'teardown_sql': None, 'teardown': None, 'current_request_set_cache': None, 'sleep': None}]

print(data)

temp = eval(data)
print(data)
