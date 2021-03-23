#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt

#读取数据
raw_data = pd.read_csv('./train.csv', usecols = ['Datetime', 'Count'])
raw_data['date'] = pd.to_datetime(raw_data['Datetime'], dayfirst = True)
raw_data.drop('Datetime',axis = 1,inplace = True)
raw_data.set_index('date', inplace = True)
#获取过去两年，也就是从2012 年 9 月至 2014 年 8月的数据
two_year_data = raw_data[(raw_data.index > pd.Timestamp('2012-08-31 23:59:59')) & 
                  (raw_data.index < pd.Timestamp('2014-09-01'))]

data = two_year_data.resample('D').sum()
data.interpolate(inplace = True)
fig = plt.figure(figsize = (20,15))
plt.plot(data['Count'])
plt.show()
fig.savefig('Original Infomation.jpg')

#从分布来看，是非平稳序列
#使用ARIMA工具，并获得最优模型
import itertools
import statsmodels.api as sm

ps = range(0,7)
qs = range(0,7)
ds = range(1,3)

parameters = itertools.product(ps,ds,qs)
parameters_list = list(parameters)
results = []
best_aic = float('inf')

for parameter in parameters_list:
    try: 
        model = sm.tsa.statespace.SARIMAX(data.Count, order = (parameter[0], parameter[1], parameter[2]),
                                          enforce_stationarity=False, enforce_invertibility=False).fit()
    except Exception as e:
        print('-'*50)
        print(parameter)
        print(e)
        continue
    aic = model.aic
    if aic < best_aic:
        best_aic = aic
        best_model = model
        best_param = parameter
    results.append([parameter, model.aic])

print('最优模型', best_model.summary())

#获取需要预测的时间段内的各日期
import calendar

def get_future_days_by_month(start,future_month):
    days = 0
    year = start.year
    month = start.month
    
    for i in range(future_month):    
        if(12 != month):
            month += 1
        else:
            month = 1
            year += 1
        days += calendar.monthrange(year, month)[1]
    return days

day_nums = get_future_days_by_month(data.index[-1], 7)
day_delta = pd.Timedelta('1D', unit = 'D')
future_date_list = []
for i in range(1, day_nums+1):
    future_date_list.append(data.index[-1] + i*day_delta)

#生成预测的数据
future = pd.DataFrame(index = future_date_list, columns = data.columns, dtype = 'int')
df = pd.concat([data, future])
df['forecast'] = best_model.get_prediction(start = 0, end = len(df)).predicted_mean
df['forecast'].iloc[0] = data['Count'].iloc[0]

#画图生成所有的数据
fig = plt.figure(figsize = (30,20))
plt.plot(df['forecast'], '-r')
plt.plot(df['Count'], '-g')
plt.show()
fig.savefig('Prediction.jpg')