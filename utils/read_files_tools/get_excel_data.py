# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/03/03
# 功能：读取excel文件

import xlrd
from typing import Text, List, Union
from utils.other_tools.models import TestCaseEnum, TestCase
from utils.cache_process.cache_control import CacheHandler
from utils.read_files_tools.get_yaml_data_analysis import CaseDataCheck


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

        """ 读取excel数据 """
        data_list = []
        data_dict = {}
        keys = self.table.row_values(0)[1:]    # 获取第一行作为key值
        data_dict['case_common'] = self.get_init    # 存入字典
        for row in range(1, self.row):
            row_dict = {}
            values = self.table.row_values(row)[1:]
            for col in range(self.col-1):
                if values[col] == '':
                    value = 'None'
                else:
                    value = values[col]
                row_dict[keys[col]] = value
            row_dict['headers'] = eval(row_dict['headers'])
            if row_dict['dependence_case_data'] != 'None':
                row_dict['dependence_case_data'] = eval(row_dict['dependence_case_data'])
            # row_dict['dependence_case_data'] = eval(row_dict['dependence_case_data'])
            row_dict['data'] = eval(row_dict['data'])
            row_dict['assert'] = eval(row_dict['assert'])
            data_list.append(row_dict)

        for i in range(len(data_list)):
            data_dict[self.get_id[i]] = data_list[i]

        return data_dict


class ExcelCaseData(CaseDataCheck):

    """ 返回用例数据内容 """
    def get_excel_data(self, case_id_switch: Union[None, bool] = None):
        yaml_data = GetExcelData(self.file_path).get_excel_data()
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
                    'is_run': self.get_run,
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


class GetTestCase:

    @staticmethod
    def case_data(case_id_lists: List):
        case_lists = []
        for i in case_id_lists:
            _data = CacheHandler.get_cache(i)
            case_lists.append(_data)

        return case_lists


if __name__ == '__main__':
    data = ExcelCaseData("\\data\\UserManger\\update_user_status.xlsx").get_excel_data()
    print(data)



