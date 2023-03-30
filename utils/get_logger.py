# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/3/12 22:22
# 功能：日志模块封装

import os
import time
import colorlog
import logging
from logging import handlers
from utils.get_path_info import GetPathInfo


class GetLogger(object):
    """ 日志封装类 """

    @classmethod
    def get_logger(cls):
        logger = logging.getLogger(__name__)  # 创建日志器
        level_relations = {
            'NOTSET': logging.NOTSET,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }  # 日志级别关系映射

        # 创建日志存放的目录
        project_path = GetPathInfo().get_project_path()
        logs_dir = project_path + "logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 日志文件以日期命名
        log_file_name = '%s.log' % time.strftime("%Y-%m-%d", time.localtime())
        log_file_path = os.path.join(logs_dir, log_file_name)

        log_colors_config = {
            'DEBUG': 'green',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        # 创建日志文件处理器
        rotating_file_handler = handlers.TimedRotatingFileHandler(filename=log_file_path,
                                                                  when='D',  # 按天分隔，一天一个文件
                                                                  interval=30,
                                                                  encoding='utf-8')

        # 创建格式器
        fmt = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(pathname)s:%(lineno)d [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S')

        sh_fmt = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(pathname)s:%(lineno)d [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config)

        # 避免重复打印日志
        if not logger.handlers:
            # 控制台输出
            console = logging.StreamHandler()  # 创建控制台日志处理器
            console.setLevel(level_relations["NOTSET"])
            console.setFormatter(fmt=sh_fmt)
            rotating_file_handler.setFormatter(fmt=fmt)
            # 写入日志文件
            logger.addHandler(console)
            logger.addHandler(rotating_file_handler)
            logger.setLevel(level_relations['DEBUG'])
        return logger


if __name__ == '__main__':
    logger = GetLogger().get_logger()
    logger.debug('调试')
    logger.info('信息')
    logger.warning('警告')
    logger.error('报错')
    logger.critical('严重')
