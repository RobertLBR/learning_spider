# 爬取北京新发地菜价
import requests
# import pymongo
import re
import time
import pandas as pd
import os
from
from elasticsearch import Elasticsearch
from elasticsearch import helpers


def get_price_data(page):
    # 定义请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
    }

    # 前端展示URL http://www.xinfadi.com.cn/priceDetail.html
    # 前端数据获取URL
    data_url = "http://www.xinfadi.com.cn/getPriceData.html"

    # 提交的表单数据，翻页
    data_form = {
        "limit": 20,
        "current": page
    }

    # 获取源码数据
    resp = requests.post(data_url, data=data_form, headers=headers).text

    # 预加载正则表达式，re.S让.能够匹配换行符
    obj = re.compile(r'"prodName":"(?P<prodName>.*?)",.*?,'
                     r'"lowPrice":"(?P<lowPrice>.*?)",'
                     r'"highPrice":"(?P<highPrice>.*?)",'
                     r'"avgPrice":"(?P<avgPrice>.*?)",.*?,'
                     r'"pubDate":"(?P<pubDate>.*?)"', re.S)

    # 根据正则表达式提取数据到迭代器中
    results = obj.finditer(resp)

    # 定义空的DataFrame
    result_pd_cnt = pd.DataFrame(columns=['prodName', 'lowPrice', 'highPrice', 'avgPrice', 'pubDate'])

    # 从迭代器中遍历出需要的数据
    for result in results:
        # 遍历出所有数据装到字典里面
        result_dic = result.groupdict()

        # 将字典数据插入到mongo数据库中
        # result_dic['pubDate'] = result_dic['pubDate'].strip('00:00:00') # strip去除括号中的内容
        # 调用mongo写入函数
        # mongo_output(result_dic)

        # 将字典数据转换为DataFrame，并追加到result_pd_cnt中
        result_pd = pd.DataFrame([result_dic])
        result_pd_cnt = result_pd_cnt.append(result_pd)

    # DataFrame数据格式化
    # 删除重复数据
    result_pd_cnt = result_pd_cnt.drop_duplicates()
    # 转换字段类型为float
    result_pd_cnt[['lowPrice', 'highPrice', 'avgPrice']] = result_pd_cnt[['lowPrice', 'highPrice', 'avgPrice']].astype(dtype=float)
    # 时间格式转换
    result_pd_cnt['pubDate'] = pd.to_datetime(result_pd_cnt['pubDate'], format='%Y-%m-%d %H:%M:%S')

    # 查看数据
    print(result_pd_cnt.info())
    print(result_pd_cnt)

    # 调用es数据库写入方法
    # save_to_es(result_pd_cnt)


def save_to_es(result):
    es = Elasticsearch([os.getenv("ES_URL")])
    print(result.info())

    actions = []
    for i in range(len(result)):
        if result.iloc[[i]].values[0][4] is not None:
            action = {
                "_index": "beijing_prices_cnt",
                "_source": {
                    u'prodName': result.iloc[[i]].values[0][0],
                    u'lowPrice': result.iloc[[i]].values[0][1],
                    u'highPrice': result.iloc[[i]].values[0][2],
                    u'avgPrice': result.iloc[[i]].values[0][3],
                    u'pubDate': result.iloc[[i]].values[0][4]
                }
            }
            actions.append(action)

    # 提交es数据
    helpers.bulk(es, actions)
    print("导入es成功")


def mongo_output(result_dic):
    try:
        # 连接mongodb
        client = pymongo.MongoClient('192.168.150.101', 30017)
        # 连接test数据库
        db = client['test']
        # 连接对应集合
        table = db['price_detail']
        # 插入result_dic数据到集合中
        table.insert_one(result_dic)
    finally:
        print('mongo资源释放')


def main():
    # 主函数调用,打印数据
    for i in range(10):
        page = i + 1
        get_price_data(page)
        print(f"收集第{page}页数据中……")
        time.sleep(2)
        # 测试用
        # break


if __name__ == '__main__':
    main()
