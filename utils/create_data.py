# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/3/11
# 功能：日志模块封装

import csv
from faker import Faker
from utils.get_path_info import GetPathInfo
from utils.get_logger import GetLogger


class CreateData:
    def __init__(self, filename, number):
        """
        :param filename:写入csv文件名
        :param number:生成数据总数
        """
        self.logger = GetLogger().get_logger()
        self.filename = filename
        self.number = number

    def create_range_data(self):

        """ 创建随机数据 """
        f = Faker(locale="zh-CN")
        data = []
        for i in range(self.number):
            address = f.address()
            pystr = f.pystr()
            row_content = address, pystr
            data.append(row_content)
        self.logger.debug(f"content: {data}")
        return data

    def save_csv_data(self, head_name):
        """
        存储数据
        :param head_name:表头名称 格式[,,,]
        """
        # 表头
        header = head_name
        self.logger.info(f"header： {header}")
        save_path_dir = GetPathInfo().get_project_path() + '/data/' + self.filename
        if len(header) == 1:
            store_info = zip(self.create_range_data())  # zip防止写入单个数据有逗号
        else:
            store_info = self.create_range_data()
        # store_data = []
        with open(save_path_dir, 'w', encoding='utf-8', newline='') as csvfile:
            # 1.创建writer对象
            writer = csv.writer(csvfile)
            # 2.写入表头
            writer.writerow(header)
            # 3.遍历每一行数据写入到csv
            for i in store_info:
                # store_data.append(i)
                writer.writerow(i)
                # store_data.clear()


if __name__ == '__main__':
    CreateData('test.csv', 10).save_csv_data(['adress', 'pystr'])

