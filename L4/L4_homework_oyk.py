# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:00:18 2021

@author: OuyangKun
"""

'''
文件读取有两种方法，实操后发现方法一明显速度快
分别两两交叉进行用时分析
'''
import time
import re
import csv
import pandas as pd

###############################################################################
#数据获取及清洗
csv_file = 'Market_Basket_Optimisation.csv'
#方法一， 鉴于本文件特点，可以直接使用文件读取的方式，获得各订单的Item，并存储在集合列表中
seperater = ',;,'

#输入：无，但需要用到全局变量csv_file
#输出：transactions, 列表的列表，其中元素为数据集中的item
#      strlist, 字符串的列表，其中字符串为'item' + seperater + 'item' +... + seperater + 'item'
def read_csv_data(): 
    #列表的列表       
    transactions = []
    #字符串列表，方便用于变成hot_encoded_df
    strlist = []
    pattern = re.compile(r'[ ]+')
    
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        #读取每一行
        for row in reader:
            tempstring = ''
            #对每行中的数据进行处理，去掉多余的空格，字符串小写
            for col in range(len(row)):
                row[col] = row[col].strip(' ')
                row[col] = row[col].rstrip(' ')
                row[col] = row[col].lower()
                row[col] = re.sub(pattern, ' ', row[col])
                tempstring += row[col]
                tempstring += seperater
            transactions.append(row)
            strlist.append(tempstring.rstrip(seperater))
    f.close()
            
    return transactions, strlist

#方法二， 利用pandas打开文件，最终得到集合
#输入：无，但需要用到全局变量csv_file
#输出：transactions, 列表的列表，其中元素为数据集中的item
def read_csv_by_pd():        
    transactions = []
    pattern = re.compile(r'[ ]+')
    data = pd.read_csv(csv_file, header = None)
    for rIndex in range(data.shape[0]):
        temp = []
        for cIndex in range(data.shape[1]):
            if str(data.loc[rIndex, cIndex]).lower() != 'nan':
                #若加入下面这句，时间+8s
                #data.loc[rIndex, cIndex] = data.loc[rIndex, cIndex].strip('')
                #若加入下面这句，时间+4.5s
                #data.loc[rIndex, cIndex] = data.loc[rIndex, cIndex].rstrip('')
                #若加入下面这句，时间+4.3s
                #data.loc[rIndex, cIndex] = data.loc[rIndex, cIndex].lower()
                #若加入下面这句，时间+4.6s，其实每句耗时都差不多
                #data.loc[rIndex, cIndex] = re.sub(pattern, ' ', data.loc[rIndex, cIndex])
                temp.append(data.loc[rIndex, cIndex])
        transactions.append(temp)
    
    return transactions   

###############################################################################
#进行关联分析
#方法一，快速apriori法
def efficient_apriori_correlation_anlysis(transactions, min_support, min_confidence): 
    from efficient_apriori import apriori    
    frequent_itemsets, rules = apriori(transactions, min_support , min_confidence)
    print('频繁项集为:', frequent_itemsets)
    print('关联规则为:', rules)
    
#方法二，标准apriori法
#输入：strlist, 字符串的列表，其中字符串为'item' + seperater + 'item' +... + seperater + 'item'
#输出：df, hot_encoded_dataframe
def get_hot_encoded_df(stringlist):
    temp = pd.Series(stringlist)
    df = temp.str.get_dummies(sep = seperater)
    return df


def apriori_correlation_anlysis(hot_encoded_df, min_support, min_confidence):
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    
    frequent_itemsets = apriori(hot_encoded_df, min_support = min_support, 
                                use_colnames = True)
    rules = association_rules(frequent_itemsets, metric="lift", 
                              min_threshold=min_confidence)
    print('频繁项集为:', frequent_itemsets)
    print('关联规则为:', rules)


#主函数
if(__name__ == '__main__'):
    print('读文件方法一，直接读取csv文件')
    time_start = time.time()
    trascation, stringlist = read_csv_data()
    time_end = time.time()
    print('耗时：', time_end - time_start)
    
    print('*'*35)
    print('读文件方法二，利用pandas读取csv文件')
    print('由于加入了字符串操作后，该方法耗时较长。')
    print('且本例中的数据较为规整，故此处不对字符产做任何操作！')
    time_start = time.time()
    trascation2 = read_csv_by_pd()
    time_end = time.time()
    print('耗时：', time_end - time_start)
    
    print('*'*35)
    print('简易Apriori算法：')
    time_start = time.time()
    efficient_apriori_correlation_anlysis(trascation, 0.02, 0.3)
    time_end = time.time()
    print('耗时：', time_end - time_start)
    
    print('*'*35)
    print('标准的Apriori算法：')
    hot_df = get_hot_encoded_df(stringlist)
    apriori_correlation_anlysis(hot_df, 0.02, 0.3)
    time_end = time.time()
    print('耗时：', time_end - time_start)
