# -*- coding:utf-8 -*-
"""
Desc : 自定义函数调用
# @Time : 2023/4/7
# @Author : Rainx
"""
import re
import datetime
import random
import time

from faker import Faker
from utils.logging_tools.log_control import INFO, ERROR
from datetime import date, timedelta, datetime
from jsonpath import jsonpath


class Context:
    """ 正则替换 """
    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    @classmethod
    def random_int(cls) -> int:
        """
        :return: 随机数
        """
        _data = random.randint(0, 5000)
        return _data

    def custom_param(self):
        """ 生成100为密码（特殊字符、数字、大写字母、小写字母）"""
        content = self.faker.password(length=100, special_chars=True,
                                      digits=True, upper_case=True, lower_case=True)
        return content

    def get_number(self) -> int:
        """ 生成纯数字"""
        _num = self.faker.random_number(6)
        return _num

    def get_char(self) -> str:
        """ 生成纯字母"""
        _char = self.faker.pystr(min_chars=None, max_chars=6)
        return _char

    def get_username(self) -> str:
        """ 生成随机用户名 """
        _str = self.faker.pystr(min_chars=None, max_chars=5)
        _num = self.faker.numerify()
        return _str + _num

    def get_password(self, length=8) -> str:
        """ 生成随机密码"""
        password = self.faker.password(length)
        return password

    def get_phone(self) -> int:
        """
        :return: 随机生成手机号码
        """
        phone = self.faker.phone_number()
        return phone

    def get_id_number(self) -> int:
        """
        :return: 随机生成身份证号码
        """
        id_number = self.faker.ssn()
        return id_number

    def get_name(self) -> str:
        """
        :return: 随机姓名
        """
        _name = self.faker.name()
        return _name

    def get_email(self) -> str:
        """
        :return: 生成邮箱
        """
        email = self.faker.free_email()
        return email

    @classmethod
    def self_operated_id(cls):
        """自营店铺 ID """
        operated_id = 212
        return operated_id

    @classmethod
    def get_time(cls) -> str:
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    def get_unixtime(self) -> int:
        """ 生成时间戳 """
        unix_time = time.time()
        return int(unix_time)

    @classmethod
    def today_date(cls):
        """获取今日0点整时间"""

        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def time_after_week(cls):
        """获取一周后12点整的时间"""

        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def host(cls) -> str:
        from utils import config
        """ 获取接口域名 """
        return config.host

    @classmethod
    def app_host(cls) -> str:
        from utils import config
        """获取app的host"""
        return config.app_host


def cache_regular(value):
    from utils.cache_process.cache_control import CacheHandler

    """
    通过正则的方式，读取缓存中的内容
    例：$cache{login_init}
    :param value:
    :return:
    """
    # 正则获取 $cache{login_init}中的值 --> login_init
    regular_dates = re.findall(r"\$cache\{(.*?)\}", value)
    # 拿到的是一个list，循环数据
    for regular_data in regular_dates:
        value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
        if any(i in regular_data for i in value_types) is True:
            value_types = regular_data.split(":")[0]
            regular_data = regular_data.split(":")[1]
            # pattern = re.compile(r'\'\$cache{' + value_types.split(":")[0] + r'(.*?)}\'')
            pattern = re.compile(r'\'\$cache\{' + value_types.split(":")[0] + ":" + regular_data + r'\}\'')
        else:
            pattern = re.compile(
                r'\$cache\{' + regular_data.replace('$', "\$").replace('[', '\[') + r'\}'
            )
        try:
            # cache_data = Cache(regular_data).get_cache()
            cache_data = CacheHandler.get_cache(regular_data)
            # 使用sub方法，替换已经拿到的内容
            value = re.sub(pattern, str(cache_data), value)
        except Exception:
            pass
    return value


def regular(target):
    """
    新版本
    使用正则替换请求数据
    :return: host
    """
    try:
        regular_pattern = r'\${{(.*?)}}'
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)   # host()
            value_types = ['int:', 'bool:', 'list:', 'dict:', 'tuple:', 'float:']
            if any(i in key for i in value_types) is True:
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                regular_int_pattern = r'\'\${{(.*?)}}\''
                target = re.sub(regular_int_pattern, str(value_data), target, 1)
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()    # Context().host()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target

    except AttributeError:
        ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确 %s", target)
        raise
    except IndexError:
        ERROR.logger.error("yaml中的 ${{}} 函数方法不正确，正确语法实例：${{get_time()}}")
        raise


if __name__ == '__main__':
    a = "${{host()}}"
    b = regular(a)
    # print(b)

