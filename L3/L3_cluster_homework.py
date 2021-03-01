# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 09:21:13 2021

@author: OuyangKun
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn import preprocessing

sns.set()
#读取数据，查看数据形态
df = pd.read_csv('car_data.csv',encoding = 'gbk', index_col = 0)
print(df.any())

#利用Z-Score进行数据规范化
preprocessing.scale(df, copy = False)

#不同K取值的误差平方和
sse = []
for k in range(1, 11):
    #k_means算法计算    
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(df)
    #计算inertia簇内误差平方和
    sse.append(kmeans.inertia_)
    
x = range(1,11)
plt.xlabel('K')
plt.ylabel('sse')
plt.plot(x, sse, 'o-')
plt.show()

#从图上看出K值取2-4时为最优点，本次取值为4
kmeans = KMeans(n_clusters = 4)
kmeans.fit(df)
predict_y = kmeans.predict(df)
df['cluster_result'] = predict_y

#输出聚类结果
print('将城市分成四类，各类的总数量如下：')
print(df.groupby('cluster_result')['人均GDP'].count())
print('将城市分成四类，各类包含的城市如下：')
df.groupby('cluster_result').apply(lambda x: print(x.index))