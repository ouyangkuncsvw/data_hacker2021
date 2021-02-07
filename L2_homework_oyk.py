# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 13:29:07 2021

@author: OuyangKun
"""
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


#获取网页内容，将所获内容保存至soup并返回
def get_html_as_soup(url):
    soup = None
    try:
        #此处如果不设置headers，在解析网页得到beautiful时，得不到第五项，也就是problem
        #利用chrome检查，发现为<td class = 'tsgztj'><span class = 'bw'> <a href = ...></a></span></td>
        #但是不设置headers，读到的soup里面会是类似于<td class = 'tsgztj'><....></td>，根本没有里面的东西
        headers={'user-agent': 
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        html = requests.get(url, headers = headers, timeout = 10)
    except Exception as e:
        print(e)
    else:
        content = html.text
        soup = BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    return soup
   

#获取表头
def get_table_head(soup):
    #需要获得得信息在class = 'tslb_b'下，而列名在th标签下
    tag = soup.find(class_ = 'tslb_b')
    table_head = tag.find_all('th')
    table_header = []
    for i in table_head:
        table_header.append(i.string)
    return table_header
     

#获取表内容
#输入：soup，每个网页对应的bs对象
#      table_head, 表头
#返回：page_df, 每个网页对应生成的DataFrame
def get_wanted_information(soup, table_head):
    page_df = pd.DataFrame()
    #需要获得得信息在class = 'tslb_b'下，而列内容在tr标签下，tr表示一行
    tag = soup.find(class_ = 'tslb_b')
    
    #获得第一行
    tr_tag = tag.table.tr.next_sibling
    while(tr_tag):
        #存储行的元素
        row = []
        #找到第一个tb元素，为投诉编号，由于最后一个元素与其他不同，需要特别处理     
        td_tag = tr_tag.td
        flag = 0
        while(td_tag):  
            if(len(table_head) -1 == flag):
                row.append(td_tag.em.string)
            else:
                row.append(td_tag.string)           
            td_tag = td_tag.next_sibling
            flag += 1
        #将行的数据生成一个df，并与page_df进行合并        
        if(len(row) == len(table_head)):
            row_df = pd.DataFrame(np.array(row)[np.newaxis,], columns = table_head)
            page_df = pd.concat([page_df, row_df])
        tr_tag = tr_tag.next_sibling
    
    return page_df


if('__main__' == __name__):
    #首页地址如下
    url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
    complains = pd.DataFrame()
    
    #url = 下一页，如果下一页表示最后一页，循环体内将url设空以退出
    #由于总共有11641页，只取前30页
    pages_num = 0
    while(url and pages_num < 30):
        soup = get_html_as_soup(url)
        if(soup):                  
            #处理本页
            #首先得到表头
            table_columns = get_table_head(soup)
            #然后每个网页都得到df，并返回            
            page_info = get_wanted_information(soup, table_columns)
            complains = pd.concat([complains, page_info])
            #找出下一页
            p_pages = soup.find(class_='p_page')
            #在此中寻找下一页的网址，如果没找到即为最后一页，退出循环        
            temp = p_pages.find(string = '下一页')
            if(temp):
                next_page = temp.parent
                suffix = next_page.get('href')
                url = url[0:url.rfind('/')] + '/' + suffix
            else:
                url = None
            pages_num +=1
        else:
            print('读取网页{0}失败！'.format(url))
            url = None    
    print(complains.shape)
    complains.index = np.arange(complains.shape[0])
    complains.to_excel('car_complain_by_spyder.xlsx')
        
    