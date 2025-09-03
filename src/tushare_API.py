# coding=utf-8
# 个股价格走势
import tushare as ts
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

def main(stock_name):
    # 日期定义
    this_day = datetime.datetime.now()
    last_month_today = (datetime.datetime.now() - datetime.timedelta(days=1095))  # 时间段选取
    to_day = this_day.strftime("%Y%m%d")
    last_day = last_month_today.strftime("%Y%m%d")

    # 加载环境变量

    load_dotenv()

    # 调用 tushare pro 接口
    pro = os.getenv("TS_PRO_API_KEY")

    # 获取个股信息
    data = pro.stock_basic(name=stock_name, list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print(data)

    # 获取个股代码
    ts_code = data.loc[0][0]

    # 获取个股明细信息
    df = pro.daily(ts_code=ts_code, start_date=last_day, end_date=to_day)
    df['交易日期'] = pd.to_datetime(df['trade_date'])  # 将object对象转化为datetime格式

    stock_data = df[['ts_code', '交易日期', 'open', 'close', 'vol', 'amount']]
    stock_data2 = df.shift(-1)   # 将时间轴往后移动一天，计算收益率
    stock_data['pg'] = (df['close'] - stock_data2['close']) * 100 / stock_data2['close'] # (当天收盘价-昨天收盘价)/昨天收盘价，计算收益率
    print("###############################统计信息##############################")
    print(stock_data.describe())
    print("###############################价格信息##############################")
    print(stock_data.head(10))

    # 绘制价格趋势图
    stock_data.plot(kind='line', x='交易日期', y='close', title=f"{stock_name}的趋势图", figsize=(10, 5))
    plt.show()

#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#查询6次，报错后重新查询
for i in range(5):
    print("第" + str(i) + "次查询----------------------")
    stock_name = str(input("请输入你需要查询的股票名字："))

    try:
        main(stock_name)
    except:
        print("没有这个股票，请重新输入")

