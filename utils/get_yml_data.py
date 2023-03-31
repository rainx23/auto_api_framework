# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/11/5 23:09
# 功能：读取yml文件 封装


import yaml
from string import Template
from utils.get_logger import GetLogger
from utils.get_path_info import GetPathInfo
from typing import Union, Text, Dict, List
from utils.models import TestCaseEnum, TestCase
from utils.read_files_tools import yaml_control


class GetYmlData:
    def __init__(self):
        self.logger = GetLogger().get_logger()
        self.case_data = None
        self.case_id = None

    @property
    def get_host(self) -> Text:
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    def get_yml_data(self, data_path, value=None):
        """
        读取yml文件 设置动态变量
        :param data_path: yml文件相对路径
        :param value: 动态变量 如：$username
        :return:
        """

        try:
            # 项目根目录
            project_path = GetPathInfo().get_project_path()
            # 根目录 + 相对路径 = 绝对路径
            yml_path = project_path + "/" + data_path
            case_list = []
            with open(yml_path, mode='r', encoding="utf-8") as f:
                text = f.read()
                if value is not None:
                    re = Template(text).safe_substitute(value)
                    json_data = yaml.safe_load(re)
                else:
                    json_data = yaml.safe_load(text)
            for key, values in json_data.items():
                if key != 'case_common':
                    self.case_data = values
                    self.case_id = key
                case_date = {
                    'url': self.get_host,
                    'method': self.case_data.get(TestCaseEnum.METHOD.value[0]),
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'requestType': self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0]).upper(),
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                    "assert_data": self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0]),
                    "title": self.case_data.get(TestCaseEnum.TITLE.value[0]),
                    "content_type": self.case_data.get(TestCaseEnum.CONTENT_TYPE.value[0])
                }
                case_list.append(TestCase(**case_date).dict())

            return case_list
        except Exception as e:
            self.logger.error(e)

    def read_yaml(self, data_path, value=None):
        try:
            # 项目根目录
            project_path = GetPathInfo().get_project_path()
            # 根目录 + 相对路径 = 绝对路径
            yml_path = project_path + "/" + data_path

            with open(yml_path, mode='r', encoding='utf-8') as f:
                value = yaml.load(stream=f, Loader=yaml.FullLoader)
                return value

        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    # data = GetYmlData().get_yml_data("data/req.yml")
    # print(data)
    # # print(GetYmlData().read_yaml("data/req.yml"))
    # # print(data['req']['url'])
    # # print(data['header'])
    # # print(data['req']['type'])
    # print(len(data))
    # for i in range(len(data)):
    #     # print(data[i])
    #     print(data[i]['req']['url'])
    data = GetYmlData().get_yml_data('data/test.yml')
    print(data)
