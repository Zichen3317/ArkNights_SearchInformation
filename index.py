# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/11/09
#             Description: 明日方舟个人中心寻访信息获取
# ==========================================
# pyqt6 ui部分
import window  # 填写导入的py文件名
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
# 数据处理部分
import ArkNights_SearchInformation
import CSVTool
from datetime import datetime
Ver = '1.0Alpha'

print("ArkNights_SearchInformation %s Service Start" % Ver)


def Get_Store(Token):
    Information_dict = ArkNights_SearchInformation.ArkNight(Token)
    print("\n[ANSI]已获取寻访信息✓ (共 %s 条记录)" %
          Information_dict['Total'])
    # 写入文件
    header = ['pool', 'name', 'rarity']
    filePath = './{}-{}-ArkNights_SearchInformation.csv'.format(str(datetime.today()).split('.')[
        0].replace(' ', '-').replace(':', '-'), Token)
    Tool = CSVTool.Tool(filePath)
    Tool.WRITE(header, {})
    Tool.ADD(Information_dict['list'])
    print("[ANSI]已完成写入✓\n文件保存至 %s" % filePath)


def Read_Analyse(CsvPath):
    '''
    CsvPath csv文件
    '''
    Data_list = CSVTool.Tool(CsvPath).READ()[1:]  # 第一个是表头，不要了
    print('\r[debug]已读取文件✓', end='')
    Rarity_3, Rarity_4, Rarity_5, Rarity_6 = 0, 0, 0, 0  # 抽出稀有度角色个数
    Character_lst, Pool_lst = [], []  # 统计角色和池子
    Character_Count_lst, Pool_Count_lst = [], []
    for i in Data_list:
        # 先统计各稀有度抽出个数
        if i[2] == '3':
            Rarity_3 += 1
        elif i[2] == '4':
            Rarity_4 += 1
        elif i[2] == '5':
            Rarity_5 += 1
        elif i[2] == '6':
            Rarity_6 += 1
        Character_lst.append(i[1])
        Pool_lst.append(i[0])

    Total = Rarity_3+Rarity_4+Rarity_5+Rarity_6  # 全部角色个数
    # 所占比重
    Rarity_3_percentage = round(Rarity_3/Total, 4)
    Rarity_4_percentage = round(Rarity_4/Total, 4)
    Rarity_5_percentage = round(Rarity_5/Total, 4)
    Rarity_6_percentage = round(Rarity_6/Total, 4)

    # 统计池子和角色个数
    Character_set = set(Character_lst)
    Pool_set = set(Pool_lst)
    for i in Character_set:
        Character_Count_lst.append([i, Character_lst.count(i)])
    for i in Pool_set:
        Pool_Count_lst.append([i, Pool_lst.count(i)])

    print('\r[debug]数据处理完毕✓', end='')
    # 数据显示
    message = '''
=====ArkNights·寻访数据分析=====
作者:ZiChen
统计文件路径:{filepath}
数据总数:{total}
-------------------------------
抽到最多的角色：{max_char}[{max_char_num}]
抽的最多的池子:{max_pool}[{max_pool_num}]
-------------------------------
三星角色抽取总数:{r3_n}[{r3_p}] 
四星角色抽取总数:{r4_n}[{r4_p}] 
五星角色抽取总数:{r5_n}[{r5_p}] 
六星角色抽取总数:{r6_n}[{r6_p}] 
===============================
'''.format(
        filepath=CsvPath,
        total=Total,
        max_char=sorted(Character_Count_lst,
                        key=lambda i: i[-1], reverse=True)[0][0],
        max_char_num=sorted(Character_Count_lst,
                            key=lambda i: i[-1], reverse=True)[0][-1],
        max_pool=sorted(
            Pool_Count_lst, key=lambda i: i[-1], reverse=True)[0][0],
        max_pool_num=sorted(
            Pool_Count_lst, key=lambda i: i[-1], reverse=True)[0][-1],
        r3_n=Rarity_3, r4_n=Rarity_4, r5_n=Rarity_5, r6_n=Rarity_6,
        r3_p=Rarity_3_percentage, r4_p=Rarity_4_percentage, r5_p=Rarity_5_percentage, r6_p=Rarity_6_percentage,
    )
    print(message)


# pyqt6 ui部分
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = window.Ui_MainWindow()  # 填写导入的py文件名以及内部类名
    ui.setupUi(MainWindow)
    MainWindow.show()

    def Get():
        Get_Store(ui.lineEdit_Token.text())

    def Analyse():
        Read_Analyse(ui.lineEdit_FilesPath.text())

    ui.pushButton_Get.clicked.connect(Get)
    ui.pushButton_Analyse.clicked.connect(Analyse)

    sys.exit(app.exec())
