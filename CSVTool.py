# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time:
#           Version:
#             Description: CSV操作（都以字典形式）
# ==========================================
import csv


class Tool:
    def __init__(self, f_path):
        '''
        初始化
        f_path CSV文件路径
        '''
        self.f_path = f_path

    def READ(self):
        with open(self.f_path, encoding="utf-8-sig", mode="r") as f:

            # 基于打开的文件，创建csv.DictReader实例
            Result_list = []
            reader = csv.reader(f)
            # 返回的对象不是list，需要解包后再返回
            for i in reader:
                Result_list.append(i)

        return Result_list

    def WRITE(self, Header_list, Content_Dict_list):
        '''
        示例
        header_list = ["设备编号", "温度", "湿度", "转速"]
        data_list = [
            {"设备编号": "0", "温度": 31, "湿度": 20, "转速": 1000},
            {"设备编号": "1", "温度": 30, "湿度": 22, "转速": 998},
            {"设备编号": "2", "温度": 32, "湿度": 23, "转速": 1005},
                ]
        '''
        with open(self.f_path, mode="w", encoding="utf-8-sig", newline="") as f:

            # 基于打开的文件，创建 csv.DictWriter 实例，将 header 列表作为参数传入。
            writer = csv.DictWriter(f, Header_list)
            # 写入 header
            writer.writeheader()
            # 写入数据
            writer.writerows(Content_Dict_list)

    def ADD(self, Content_list):
        with open(self.f_path, mode="a+", encoding="utf-8-sig", newline="") as f:

            # 基于打开的文件，创建 csv.DictWriter 实例，将 header 列表作为参数传入。
            Writer = csv.writer(f)
            # 写入数据
            Writer.writerows(Content_list)
