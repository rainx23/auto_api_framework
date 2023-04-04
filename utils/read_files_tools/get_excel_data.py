# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/03/03
# 功能：读取excel文件 封装

import xlrd
from utils.logging_tools.log_control import INFO, ERROR, WARNING
from config.setting import ensure_path_sep


class GetExcelData:
    def __init__(self, data_path, sheet_name='Sheet1'):
        """
        初始化方法
        :param data_path:excel文件相对路径
        :param sheet_name:excel访问的sheet名 默认为Sheet1
        """
        self.excel_path = ensure_path_sep(data_path)
        self.workbook = xlrd.open_workbook(self.excel_path)
        self.table = self.workbook.sheet_by_name(sheet_name=sheet_name)
        self.row = self.table.nrows     # 获取总行数
        self.col = self.table.ncols     # 获取总列数

    def get_excel_data(self):
        """
        读取excel数据
        """
        try:
            if self.row <= 1:
                WARNING.logger.warning('总行数小于1，请添加内容')
            else:
                keys = self.table.row_values(0)     # 获取第一行作为key值
                print(keys)
                if isinstance(keys, str):
                    keys = self.table.row_values(0).replace('\n', ' ')
                print(keys)
                data_list = []
                for row in range(1, self.row):
                    dict = {}
                    values = self.table.row_values(row)
                    for col in range(self.col):
                        value = values[col]
                        if isinstance(values[col], float):
                            value = int(values[col])
                            if float(value) != values[col]:
                                value = values[col]
                        if isinstance(values[col], str):
                                value = values[col].replace('\n', ' ')
                        dict[keys[col]] = value
                    data_list.append(dict)

                return data_list

        except Exception as e:
            ERROR.logger.error(e)


if __name__ == '__main__':
    data = GetExcelData("\\data\\test_datas.xls", 'test').get_excel_data()
    print(data)


