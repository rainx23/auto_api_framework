# -*- coding:utf-8 -*-
"""
Desc : 自定义函数调用
# @Time : 2022/4/2 9:32 上午
# @Author : 余少琪
"""
import re
import datetime
import random
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

    def get_female_name(self) -> str:
        """

        :return: 女生姓名
        """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """

        :return: 男生姓名
        """
        male_name = self.faker.name_male()
        return male_name

    def get_email(self) -> str:
        """

        :return: 生成邮箱
        """
        email = self.faker.email()
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
                    print(value_data)
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
    a = "${{host()}} aaa"
    b = regular(a)

