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
from time import localtime, strftime
Ver = '1.3.1Alpha'

print("ArkNights_SearchInformation %s Service Start" % Ver)


def Merge(Path: list):
    '''
    合并多个寻访记录表
    '''
    print('[Debug]共有%s个文件' % len(Path))
    Total_lst = []  # 用于合并的列表
    header = ['pool', 'name', 'rarity', 'ts']
    for i in Path:
        for j in CSVTool.Tool(i).READ()[1:]:  # 第一个是表头，不要了
            # 后面要去除重复项需要用到set()，但set()规定列表内不能有可变元素（元组是不可变元素）
            Total_lst.append(tuple(j))
    Total_lst = set(Total_lst)  # 删除重复项
    # 重新将内部元素转为列表
    Temp_lst = []
    for i in Total_lst:
        Temp_lst.append(list(i))
    # 排序
    Total = sorted(Total_lst, key=lambda i: i[-1], reverse=True)
    filePath = 'Merge-{}.csv'.format(str(datetime.today()).split('.')[
        0].replace(' ', '-').replace(':', '-'))
    Tool = CSVTool.Tool(filePath)
    Tool.WRITE(header, {})
    Tool.ADD(Total)
    print("[ANSI]已完成合并✓\n文件保存至 %s" % filePath)


def Get_Store(Token: str):
    Information_dict = ArkNights_SearchInformation.ArkNight(Token)
    print("\n[ANSI]已获取寻访信息✓ (共 %s 条记录)" %
          Information_dict['Total'])
    # 写入文件
    header = ['pool', 'name', 'rarity', 'ts']
    filePath = './{}-{}-ArkNights_SearchInformation.csv'.format(str(datetime.today()).split('.')[
        0].replace(' ', '-').replace(':', '-'), Token)
    Tool = CSVTool.Tool(filePath)
    Tool.WRITE(header, {})
    Tool.ADD(Information_dict['list'])
    print("[ANSI]已完成写入✓\n文件保存至 %s" % filePath)


def Read_Analyse(CsvPath: str):
    '''
    CsvPath csv文件
    '''
    Data_list = CSVTool.Tool(CsvPath).READ()[1:]  # 第一个是表头，不要了
    print('\r[debug]已读取文件✓', end='')
    Rarity_3, Rarity_4, Rarity_5, Rarity_6 = 0, 0, 0, 0  # 抽出稀有度角色个数
    Character_lst, Pool_lst = [], []  # 统计角色和池子
    Pool_Count_lst = []
    # 六星和五星池子
    Six_Character_lst, Five_Character_lst = [], []
    for i in Data_list:
        # 先统计各稀有度抽出个数
        if i[2] == '3':
            Rarity_3 += 1
        elif i[2] == '4':
            Rarity_4 += 1
        elif i[2] == '5':
            Rarity_5 += 1
            Five_Character_lst.append(i[1])
        elif i[2] == '6':
            Rarity_6 += 1
            Six_Character_lst.append(i[1])
        Character_lst.append(i[1])
        Pool_lst.append(i[0])

    Total = Rarity_3+Rarity_4+Rarity_5+Rarity_6  # 全部角色个数
    # 所占比重

    Rarity_3_percentage = round((Rarity_3/Total)*100, 2)
    Rarity_4_percentage = round((Rarity_4/Total)*100, 2)
    Rarity_5_percentage = round((Rarity_5/Total)*100, 2)
    Rarity_6_percentage = round((Rarity_6/Total)*100, 2)
    #print('\n[debug]3:{}-{} 4:{}-{}'.format(Rarity_3,Rarity_3_percentage, Rarity_4, Rarity_4_percentage))
    # 统计池子个数
    Pool_set = set(Pool_lst)
    for i in Pool_set:  # [池子名称,抽数]
        Pool_Count_lst.append([i, Pool_lst.count(i)])

    # 统计六星出货数据
    Six_Character_data = ''
    Six_Character_set = set(Six_Character_lst)
    for i in Six_Character_set:  # [池子名称,抽数]
        Six_Character_data += '%s[%s]\n' % (i, Character_lst.count(i))
    # 统计五星出货数据
    Five_Character_data = ''
    Five_Character_set = set(Five_Character_lst)
    for i in Five_Character_set:  # [池子名称,抽数]
        Five_Character_data += '%s[%s]\n' % (i, Character_lst.count(i))

# 将池子名称和抽数合并为一个字符串
    Pool_data = ''
    for i in Pool_Count_lst:
        Pool_data += '%s:总 %s抽\n' % (i[0], i[1])

    # 角色同理
    message = '''
-----明日方舟寻访分析----
统计时间区间 {starttime} - {endtime}

----总计: {Total} 抽----
6星 {Six}人 概率 {SixP}%
5星 {Five}人 概率 {FiveP}%
4星 {Four}人 概率 {FourP}%
3星 {Three}人 概率 {ThreeP}%

--------平均出货--------
6星 {SixAve}抽
5星 {FiveAve}抽

--------卡池数据--------
{Pool_data}
------六星出货记录------
{Six_Character_data}
------五星出货记录------
{Five_Character_data}
    '''.format(
        starttime=strftime("%m月%d日 %H:%M:%S",
                           localtime(int(Data_list[-1][-1]))),
        endtime=strftime("%m月%d日 %H:%M:%S", localtime(int(Data_list[0][-1]))),
        Total=Total, Six=Rarity_6, Five=Rarity_5, Four=Rarity_4, Three=Rarity_3,
        SixP=Rarity_6_percentage, FiveP=Rarity_5_percentage, FourP=Rarity_4_percentage, ThreeP=Rarity_3_percentage,
        SixAve=round(Total/Rarity_6, 1), FiveAve=round(Total/Rarity_5, 1),
        Pool_data=Pool_data,
        Six_Character_data=Six_Character_data,
        Five_Character_data=Five_Character_data,
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
        '''
        pyqt5 接口函数
        '''
        Get_Store(ui.lineEdit_Token.text())

    def Analyse():
        '''
        pyqt5 接口函数
        '''
        Read_Analyse(ui.lineEdit_FilesPath.text())

    def Merge_IN():
        '''
        pyqt5 接口函数
        '''
        Merge(ui.textEdit_merge_filepath.toPlainText().split('|'))

    ui.pushButton_Get.clicked.connect(Get)
    ui.pushButton_Analyse.clicked.connect(Analyse)
    ui.pushButton_merge.clicked.connect(Merge_IN)

    sys.exit(app.exec())
