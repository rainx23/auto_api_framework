# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/03/03
# 功能：读取excel文件

import xlrd
import os
from typing import Text, List, Union
from utils.other_tools.models import TestCaseEnum, TestCase
from config.setting import ensure_path_sep
from utils.other_tools.models import Method, RequestType
from utils.cache_process.cache_control import CacheHandler


class CaseDataCheck:
    """ 用例数据校验 """
    def __init__(self, file_path):
        self.file_path = ensure_path_sep(file_path)
        if os.path.exists(self.file_path) is False:
            raise FileNotFoundError(f"用例地址 {self.file_path} 未找到")

        self.case_data = None
        self.case_id = None

    def _assert(self, attr: Text):
        assert attr in self.case_data.keys(), (
            f"用例ID为 {self.case_id} 的用例中缺少 {attr} 参数，请确认用例内容是否编写规范."
            f"当前用例文件路径：{self.file_path}"
        )

    def check_params_exit(self):
        # 映射获取枚举key [('host', True), ('url', True),....]
        for enum in list(TestCaseEnum._value2member_map_.keys()):
            if enum[1]:
                self._assert(enum[0])

    def check_params_right(self, enum_name, attr):
        _member_names_ = enum_name._member_names_
        assert attr.upper() in _member_names_, (
            f"用例ID为 {self.case_id} 的用例中 {attr} 填写不正确，"
            f"当前框架中只支持 {_member_names_} 类型."
            f"如需新增 method 类型，请联系管理员."
            f"当前用例文件路径：{self.file_path}"
        )
        return attr.upper()

    @property
    def get_method(self) -> Text:
        return self.check_params_right(
            Method,
            self.case_data.get(TestCaseEnum.METHOD.value[0])
        )

    @property
    def get_host(self) -> Text:
        host = (
                self.case_data.get(TestCaseEnum.HOST.value[0]) +
                self.case_data.get(TestCaseEnum.URL.value[0])
        )
        return host

    @property
    def get_dependence_case_data(self):
        _dep_data = self.case_data.get(TestCaseEnum.DE_CASE.value[0])
        if _dep_data:
            assert self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0]) is not None, (
                f"程序中检测到您的 case_id 为 {self.case_id} 的用例存在依赖，但是 {_dep_data} 缺少依赖数据."
                f"如已填写，请检查缩进是否正确， 用例路径: {self.file_path}"
            )
        return self.case_data.get(TestCaseEnum.DE_CASE_DATA.value[0])

    @property
    def get_request_type(self) -> Text:
        return self.check_params_right(
            RequestType,
            self.case_data.get(TestCaseEnum.REQUEST_TYPE.value[0])
        )

    @property
    def assert_data(self) -> Text:
        _assert_data = self.case_data.get(TestCaseEnum.ASSERT_DATA.value[0])
        assert _assert_data is not None, (
            f"用例ID 为 {self.case_id} 未添加断言，用例路径: {self.file_path}"
        )
        return _assert_data


class GetExcelData:
    def __init__(self, file_path):
        self.workbook = xlrd.open_workbook(file_path)
        self.table = self.workbook.sheets()[1]
        self.row = self.table.nrows     # 获取总行数
        self.col = self.table.ncols     # 获取总列数
        self.data_dict = {}

    @property
    def get_init(self):
        tables = self.workbook.sheet_by_index(0)
        rows = tables.nrows
        init_dict = {}
        for i in range(rows):
            config_data = tables.row_values(i)
            init_dict[config_data[0]] = config_data[1]
        return init_dict

    @property
    def get_id(self):
        ids = self.table.col_values(0)[1:]
        return ids

    def get_excel_data(self):
        """
        读取excel数据
        """
        data_list = []
        data_dict = {}
        keys = self.table.row_values(0)[1:]    # 获取第一行作为key值
        if isinstance(keys, str):
            keys = self.table.row_values(0).replace('\n', ' ')
        data_dict['case_common'] = self.get_init
        for row in range(1, self.row):
            row_dict = {}
            values = self.table.row_values(row)[1:]
            for col in range(self.col-1):
                if values[col] == '':
                    value = 'None'
                else:
                    value = values[col]
                row_dict[keys[col]] = value

            data_list.append(row_dict)

        for i in range(len(data_list)):
            data_dict[self.get_id[i]] = data_list[i]
        return data_dict


class CaseData(CaseDataCheck):

    """ 返回用例数据内容 """
    def get_excel_data(self, case_id_switch: Union[None, bool] = None):
        yaml_data = GetExcelData(self.file_path).get_excel_data()
        print(yaml_data)
        case_list = []
        for key, values in yaml_data.items():
            # 公共配置中的数据，与用例数据不同，需要单独处理
            if key != 'case_common':
                self.case_data = values
                self.case_id = key
                super().check_params_exit()
                case_date = {
                    'url': self.get_host,
                    'method': self.get_method,
                    "detail": self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                    'headers': self.case_data.get(TestCaseEnum.HEADERS.value[0]),
                    'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),
                    'requestType': super().get_request_type,
                    'data': self.case_data.get(TestCaseEnum.DATA.value[0]),
                    'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),
                    'dependence_case_data': self.get_dependence_case_data,
                    "assert_data": self.assert_data,
                }
                if case_id_switch is True:
                    case_list.append({key: TestCase(**case_date).dict()})
                else:
                    case_list.append(TestCase(**case_date).dict())

        return case_list


if __name__ == '__main__':
    # data = GetExcelData("\\test.xlsx", '创建用户').get_excel_data()
    # print(data)
    data = CaseData("\\data\\UserManger\\update_user_status.xlsx").get_excel_data()
    print(data)


