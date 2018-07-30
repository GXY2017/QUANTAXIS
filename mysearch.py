
# coding: utf-8

# In[ ]:

import requests
import re
import json
import sys
import os
#from prettyPrint import (INFO, ERROR)
import time
from lxml import html,etree
from bs4 import BeautifulSoup
import pandas as pd


"""搜狗指数_微信"""
def sougou_wechat(keyword,address):
    url1 = 'http://index.sogou.com/index/media/wechat'  
    params = {'kwdNamesStr': keyword, ##只能一个个查询
              'timePeriodType': 'MONTH',
              'dataType': 'MEDIA_WECHAT',
              'queryType': 'INPUT',
              }

    """接口与报错提示"""
    def R(text, end='\n'): print('\033[0;31m{}\033[0m'.format(text), end=end)
    def G(text, end='\n'): print('\033[0;32m{}\033[0m'.format(text), end=end)

    page = requests.get(url1, params=params)
    if page.status_code != 200:
        R('ERROR 状态码:{}'.format(result.status_code))
        sys.exit()
    G('OK!')

    """处理收到的页面信息"""    
    soup = BeautifulSoup(page.content,'html5lib')
    scriptStr = soup.script.get_text()

    #data = re.findall(r'root\.SG\.data\s=\s(.+?);', scriptStr)[0]
    Data = re.findall(r'root\.SG\.wholedata\s=\s(.+?);', scriptStr)[0] 
    DataJson = json.loads(Data)

    """装载到DATAFRAME中去"""
    Datadf = pd.DataFrame()  ## 设一个空的DF
    j = 0
    for DataItem in DataJson['pvList'][0]:
        DataOne = pd.DataFrame.from_dict(DataItem, orient='index')
        Datadf = pd.concat([Datadf,DataOne],axis=1,sort=False) ## sort字段接受未来版本的默认顺序
        j = j + 1

    """清理数据，按DF格式输出"""    
    result = (Datadf.T[['pv','date']])
    result['date'] = pd.to_datetime(result['date'], format='%Y%m%d.0')
    result = result.set_index(['date'])

    """保存到CSV"""


    ###获得本地CSV数据，若不存在本地文件，则新建一个。若存在本地文件，则把新数据合并到已有数据中。
    
    if os.path.exists(address) == False:
        pd.DataFrame(columns=['date', 'pv']).to_csv(address,index=False)
        f = open(address)  ## 文件名中有中文，必须用函数打开文件
        data_local = pd.read_csv(f)
        data_local = data_local.set_index('date')
        data_local.index = pd.to_datetime(data_local.index)
        f.close()  ## 不要忘记关闭文件
        print('没有原文件，新生成一个文件')
    else:  
        f = open(address)
        data_local = pd.read_csv(f)
        data_local = data_local.set_index('date')
        data_local.index = pd.to_datetime(data_local.index)
        f.close()
        print('已读取本地文件')
        #data_local = pd.read_csv(address)

    new_local = pd.concat([data_local,result]).drop_duplicates()
    new_local.to_csv(address)
    return print("""已更新""")


"""搜狗指数_全部"""
def sougou_all(keyword,address):
    url1 = 'http://index.sogou.com/index/searchHeat'  
    params = {'kwdNamesStr': keyword, ##只能一个个查询
              'timePeriodType': 'MONTH',
              'dataType': 'SEARCH_ALL',
              'queryType': 'INPUT',
              }

    """接口与报错提示"""
    def R(text, end='\n'): print('\033[0;31m{}\033[0m'.format(text), end=end)
    def G(text, end='\n'): print('\033[0;32m{}\033[0m'.format(text), end=end)

    page = requests.get(url1, params=params)
    if page.status_code != 200:
        R('ERROR 状态码:{}'.format(result.status_code))
        sys.exit()
    G('OK!')

    """处理收到的页面信息"""    
    soup = BeautifulSoup(page.content,'html5lib')
    scriptStr = soup.script.get_text()

    #data = re.findall(r'root\.SG\.data\s=\s(.+?);', scriptStr)[0]
    Data = re.findall(r'root\.SG\.wholedata\s=\s(.+?);', scriptStr)[0] 
    DataJson = json.loads(Data)

    """装载到DATAFRAME中去"""
    Datadf = pd.DataFrame()  ## 设一个空的DF
    j = 0
    for DataItem in DataJson['pvList'][0]:
        DataOne = pd.DataFrame.from_dict(DataItem, orient='index')
        Datadf = pd.concat([Datadf,DataOne],axis=1,sort=False) ## sort字段接受未来版本的默认顺序
        j = j + 1

    """清理数据，按DF格式输出"""    
    result = (Datadf.T[['pv','date']])
    result['date'] = pd.to_datetime(result['date'], format='%Y%m%d')
    result = result.set_index(['date'])

    """保存到CSV"""


    ###获得本地数据
    if os.path.exists(address) == False:
        pd.DataFrame(columns=['date', 'pv']).to_csv(address,index=False)
        f = open(address)  ## 文件名中有中文，必须用函数打开文件
        data_local = pd.read_csv(f)
        data_local = data_local.set_index('date')
        data_local.index = pd.to_datetime(data_local.index)
        f.close()  ## 不要忘记关闭文件
        print('没有原文件，新生成一个文件')
    else:  
        f = open(address)
        data_local = pd.read_csv(f)
        data_local = data_local.set_index('date')
        data_local.index = pd.to_datetime(data_local.index)
        f.close()
        print('已读取本地文件')
        #data_local = pd.read_csv(address)

    new_local = pd.concat([data_local,result]).drop_duplicates()
    new_local.to_csv(address)
    return print("""已更新""")


"""打开搜狗下载的CSV文件"""
def open_sougou(address):
    f = open(address)
    data = pd.read_csv(f).set_index('date')
    data.index = pd.to_datetime(data.index)
    f.close()
    return data['pv']
