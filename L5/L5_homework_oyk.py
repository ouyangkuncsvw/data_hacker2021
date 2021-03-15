# -*- coding: utf-8 -*-
"""
Created on Mon Mar  15 9:00:18 2021

@author: OuyangKun
"""
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

###############################################################################
#数据获取及清洗
csv_file = 'Market_Basket_Optimisation.csv'
seperater = ',;,'

#输入：无，但需要用到全局变量csv_file
#输出：strlist, 字符串的列表，其中字符串为'item' + seperater + 'item' +... + seperater + 'item'
def read_csv_data(file): 
    #字符串列表，方便用于变成hot_encoded_df
    strlist = []
    pattern = re.compile(r'[ ]+')
    
    if(file):        
        with open(file, 'r') as f:
            reader = csv.reader(f)
            #读取每一行
            for row in reader:
                tempstring = ''
                #对每行中的数据进行处理，去掉多余的空格，字符串小写
                for i in range(len(row)):
                    row[i] = row[i].strip(' ')
                    row[i] = row[i].rstrip(' ')
                    row[i] = row[i].lower()
                    row[i] = re.sub(pattern, ' ', row[i])
                    tempstring += row[i]
                    tempstring += seperater
                strlist.append(tempstring.rstrip(seperater))
        f.close()
            
    return strlist 

#输入：strlist,字符串的列表，其中字符串为'item' + seperater + 'item' +... + seperater + 'item'
#输出：df, DataFrame， hot_encoded
def get_hot_encoded_df(stringlist):
    temp = pd.Series(stringlist)
    df = temp.str.get_dummies(sep = seperater)
    return df


# 去掉停用词
def remove_stop_words(f):
	stop_words = ['ground']
	for stop_word in stop_words:
		f = f.replace(stop_word, '')
	return f

#生成词云并画图
def create_word_cloud(f):
    f = remove_stop_words(f)
    #下面两句的目的是什么呀？
    #cut_text = word_tokenize(f)
    #cut_text = " ".join(cut_text)  
    wc = WordCloud(max_words = 100, width = 2000, height = 1200)
    wordcloud = wc.generate(f)
    wordcloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

#画柱状图
def draw_bars(items, counts):
    fig = plt.figure(figsize = (20, 12))
    ax = plt.axes([0.1, 0.15, 0.8,0.8])
    ax.bar(items, counts, width = 0.8, bottom = 0, align = 'center')
    #优化显示格式
    ax.set(title = 'Top 20 Pupular Goods', xlabel = 'Goods', ylabel = 'Purchasing Frequency')
    ax.tick_params(axis = 'x', labelrotation = 45)
    #ax.set_title('Top 20 Pupular Goods')
    #ax.set_xlabel()
    fig.savefig('Bars.jpg')
    plt.show()
    
    
#主函数
if(__name__ == '__main__'):
    #读取文件
    stringlist = read_csv_data(csv_file)
    #生成词云
    strTemp = ''.join(stringlist)
    create_word_cloud(strTemp)
    #数据变成encoded形式
    hot_df = get_hot_encoded_df(stringlist)
    #计算各元素出现的次数
    item_count = hot_df.sum()
    item_count.sort_values(ascending = False, inplace = True)
    item_count = item_count/hot_df.shape[0]
    #将前20名的item和数量生成柱状图
    draw_bars(item_count[:20].index, item_count[:20].values)