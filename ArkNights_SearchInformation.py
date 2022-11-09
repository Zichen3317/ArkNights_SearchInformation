# -*- coding:utf-8 -*-
# ==========================================
#       Author: ZiChen
#        📧Mail: 1538185121@qq.com
#         ⌚Time: 2022/11/09
#           Version:
#             Description:明日方舟个人中心寻访信息api（重构数据输出）
# ==========================================
from urllib import request
import json


def ArkNight(token):
    '''
    Url 获取到的寻访信息token
    E.G https://ak.hypergryph.com/user/api/inquiry/gacha?page=2&token=XVQkRmXKi6HOMi7kKnhBKsh5&channelId=1
    输出数据示例
    {'Total':10,'list':[['斩荆辟路','梅',4],['斩荆辟路','地灵',4]]}
    '''
    Out_Result_Dict = {}  # 输出用字典
    Temp_Result_Lst = []  # 存数据的
    PageNum = 1
    while True:
        headers = {  # 请求的头部
            'referer': "https://ak.hypergryph.com/user/inquiryGacha",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        }

        Url = 'https://ak.hypergryph.com/user/api/inquiry/gacha?page={}&token={}&channelId=1'.format(
            PageNum, token)
        req = request.Request(url=Url, headers=headers)  # GET无data项
        res = request.urlopen(req)
        res = str(res.read(), encoding='utf-8')  # 将返回的bytes类型转为str类型
        data = json.loads(res)['data']  # 如果是json/dict类型,这一步可以转为dict类型,前提是从str转
        if PageNum == 1:  # 第一页的时候把数据总数获取了，后面就不重复获取了
            Out_Result_Dict['Total'] = data['pagination']['total']
        else:
            pass
        if len(data['list']) == 0:  # 超数据了，故列表内无数据，此时结束循环
            break
        else:  # 没超，重构数据
            for i in data['list']:
                for j in i['chars']:  # 如果一次十抽的话会存十个数据
                    Temp_Result_Lst.append([i['pool'],  # 池子名称
                                            j['name'],  # 角色名
                                            # 星级，返回的星级都-1，故+1还原
                                            int(j['rarity']) + 1,
                                            ])
            print('\r[debug]已获取第%s页信息' % PageNum, end='')  # 覆盖打印
            PageNum += 1
    # 循环结束后进行数据统合并返回
    Out_Result_Dict['list'] = Temp_Result_Lst
    return Out_Result_Dict
