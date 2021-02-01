# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:27:58 2021

@author: OuyangKun
"""

import numpy as np
import pandas as pd


seperator = '*'*68

'''
Action 1: 求2+4+6+8+...+100的求和
'''
print('--  Action 1  --')
#method 1
a = sum(range(2,101,2))
print('method 1 output:{0}'.format(a))
#method 2
a = np.sum(np.arange(2, 101, 2))
print('method 2 output:{0}'.format(a))
print(seperator)


'''
Action 2: 统计成绩
            语文、英语、数学的平均成绩、最小成绩、最大成绩、方差、标准差
            按总成绩排序，得出名次进行成绩输出
姓名        语文        数学        英语
张飞        68          65          30
关羽        95          76          98
刘备        98          86          88
典韦        90          88          77
许褚        80          90          90

'''
print('--  Action 2  --')
scores = pd.DataFrame({'姓名':['张飞','关羽','刘备', '典韦', '许褚'],
                       '语文':[68, 95, 98, 90, 80],
                       '数学':[65, 76, 86, 88, 90],
                       '英语':[30, 98, 88, 77, 90]})
scores_overview = scores.describe()
temp_string = '同学们{0}科目的平均成绩、最小成绩、最大成绩、方差，标准差为：'

for col in scores_overview.columns:
    print(temp_string.format(col))
    print(scores_overview.loc['mean',col], '\t',
          scores_overview.loc['min', col], '\t',
          scores_overview.loc['max', col], '\t',
          round(scores_overview.loc['std', col],2), '\t',
          round(scores_overview.loc['std', col]**0.5,2), '\t')

print('总成绩排名:')
scores['总成绩'] = scores['语文'] + scores['数学'] + scores['英语']
print(scores.sort_values('总成绩', ascending = False)['姓名'].values)
print(seperator)


'''
Action 3: 对汽车质量数据进行统计：
            哪个品牌投诉总数、车型投诉总数、品牌平均车型投诉总数最多
'''
print('--  Action 3  --')
#step 1: 数据加载，数据存放在相同目录下中，名为'car_complain.csv'
complains = pd.read_csv('car_complain.csv')

#step 2: 数据预处理及数据清洗
#查看数据，发现75个品牌中，“一汽大众”和"一汽-大众"应是同一个品牌
#将"一汽-大众"替换成"一汽大众"
complains.loc[complains['brand'] == '一汽-大众', 'brand'] = '一汽大众'

#由于只需要计算问题数，不需要针对每种问题进行数据分析，
#因此可以将'problem'中的值进行区分计数，换算成存在多少问题数
complains['p_num'] = complains['problem'].str.split(',').apply(
                        lambda x: len(x)-1)

#step3:品牌投诉总数、车型投诉总数、品牌平均车型投诉总数
#利用前面得到的问题数直接计算
brand_overview = complains.groupby('brand').apply(
                    lambda x: np.sum(x['p_num'])).sort_values(ascending = False)
print('品牌投诉总数最多的为{0}, 数量为{1}个！'.format(
                    brand_overview.index[0], brand_overview[0]))

model_overview = complains.groupby('car_model').apply(
                    lambda x: np.sum(x['p_num'])).sort_values(ascending = False)
print('车型投诉总数最多的为{0}, 数量为{1}个！'.format(
                    model_overview.index[0], model_overview[0]))

brand_model_overview = complains.groupby('brand').apply(
                            lambda x: x['p_num'].sum()/x['car_model'].count()
                        ).sort_values(ascending = False)
print('品牌平均车型投诉总数最多的为{0}, 数量为{1}个！'.format(
                    brand_model_overview.index[0], brand_model_overview[0]))

print(seperator)

##############################################################################
print('拆分problem字段，以用于后续按照缺陷类型来从品牌、车型方面进行统计!')
#用于存储prolbem都有哪些缺陷代码的集合
temp_set = set()
for p in complains['problem'].str[:-2].str.split(','):
    for i in p:
        temp_set.add(i)
        
#创建DF, columns为各种缺陷代码，行数为complain行数，内容为0
data = pd.DataFrame(np.zeros((complains.shape[0], len(temp_set)), dtype = int),
                    columns = temp_set)

#进行计算，如果data列名在complain['problem']中存在，则计数变为1
complains_new = pd.merge(complains, data, left_index = True, right_index = True)

for row in range(complains_new.shape[0]):
    for col in data.columns:
        if col in complains_new.loc[row, 'problem'].split(','):
            complains_new.loc[row, col] = 1
            
print('拆分后数据的形状为', complains_new.shape)
print('拆分后数据的列为', complains_new.columns)
print('拆分后数据"H93"总抱怨数为', complains_new['H93'].sum())


#下面的语句为何会有语法错误?
for col in data.columns:
    complain_new[col].apply(lambda x: x[col] = 1 if col in x['problem'].str.split())

 
    
    
    

      















