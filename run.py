# -*- coding:utf-8 -*-
# 作者：Rainx
# 时间：2023/3/15 16:40
# 功能：批量执行测试用例，并生成Allure测试报告

import os
import traceback
import pytest
from utils.notify.ding_talk import DingTalkSendMsg
from utils.notify.lark import FeiShuTalkChatBot
from utils.other_tools.allure_data.allure_report_data import AllureFileClean
from models import NotificationType
from notify.send_email import SendEmail
from read_files_tools.case_automatic_control import TestCaseAutomaticGeneration
from utils.notify.wechat_send import WeChatSend
from utils.other_tools.allure_data.error_case_excel import ErrorCaseExcel
from utils import config


class Run:
    @staticmethod
    def run_default():

        try:
            # 判断现有的测试用例，如果未生成测试代码，则自动生成
            TestCaseAutomaticGeneration().get_case_automatic()

            # 定义PyTest运行参数
            # 运行 pytest，并把 Allure 原始结果写入 ./report/tmp。
            pytest.main(['-s', '-W', 'ignore:Module already imported:pytest.PytestWarning',
                         '--alluredir', './report/tmp', "--clean-alluredir"])

            # 执行用例，并生成测试报告
            # 调用本机安装的 allure 命令，把原始结果生成 HTML 报告。
            os.system(r"allure generate ./report/tmp -o ./report/html --clean")

            allure_data = AllureFileClean().get_case_count()
            # 根据 config.yaml 中的 notification_type 决定是否发送钉钉/企微/邮件/飞书通知。
            notification_mapping = {
                NotificationType.DING_TALK.value: DingTalkSendMsg(allure_data).send_ding_notification,
                NotificationType.WECHAT.value: WeChatSend(allure_data).send_wechat_notification,
                NotificationType.EMAIL.value: SendEmail(allure_data).send_main,
                NotificationType.FEI_SHU.value: FeiShuTalkChatBot(allure_data).post
            }

            # 判断是否发送报告通知
            if config.notification_type != NotificationType.DEFAULT.value:
                notify_type = config.notification_type.split(",")
                for i in notify_type:
                    notification_mapping.get(i.lstrip(""))()

            # 收集异常用例内容
            if config.excel_report:
                ErrorCaseExcel().write_case()

        except Exception:
            # 如有异常，相关异常发送邮件
            e = traceback.format_exc()
            send_email = SendEmail(AllureFileClean.get_case_count())
            send_email.error_mail(e)
            raise


if __name__ == '__main__':
    Run().run_default()
