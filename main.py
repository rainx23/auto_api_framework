# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2022/3/14 20:45
# 功能：测试用例

from faker import Faker

f = Faker(locale='zh_CN')
print(f.password(length=10,special_chars=False))
print(f.pystr(min_chars=None, max_chars=5))

def te(length=10,special_chars=True, digits=True, upper_case=True, lower_case=True):
    f = Faker(locale='zh_CN')
    print(f.password(length, special_chars, digits, upper_case, lower_case))


te(length=4)


url = "/api/private/v1/users/$url_param{id}"
print(url.replace("$url_param{id}", "258"))
