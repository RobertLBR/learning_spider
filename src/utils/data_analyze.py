# 菜价数据分析
import pymongo
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def mongo_output():
    try:
        # 连接数据mongodb
        client = pymongo.MongoClient('192.168.150.101', 30017)

        db = client['test']

        # 连接对应表
        table = db['price_detail']

        # 数据转换为DataFrame
        result = pd.DataFrame(table.find())
        # result.info()

        # 数据清洗
        del result['_id']  # 删除_id列
        result = result.drop_duplicates()  # 删除重复数据
        # 转换字段类型为float
        result[['lowPrice', 'highPrice', 'avgPrice']] = result[['lowPrice', 'highPrice', 'avgPrice']].astype(dtype=float)

        # 时间格式转换
        result['pubDate'] = result['pubDate'] + "00:00:00"
        result['pubDate'] = pd.to_datetime(result['pubDate'], format='%Y-%m-%d %H:%M:%S')

        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)
        # 设置value的显示长度为100，默认为50
        pd.set_option('max_colwidth', 100)

        # 数据概要
        print(result.describe())
        print(result.sort_values('avgPrice', ascending=False).head(10))

        # # save to ES
        # es = Elasticsearch(['http://elastic:x2ZaY8pc6LN55kA4M08b00KJ@192.168.150.101:30200'])
        #
        # actions = []
        # for i in range(len(result)):
        #     if result.iloc[[i]].values[0][4] is not None:
        #         action = {
        #             "_index": "beijing_prices",
        #             "_source": {
        #                 u'prodName': result.iloc[[i]].values[0][0],
        #                 u'lowPrice': result.iloc[[i]].values[0][1],
        #                 u'highPrice': result.iloc[[i]].values[0][2],
        #                 u'avgPrice': result.iloc[[i]].values[0][3],
        #                 u'pubDate': result.iloc[[i]].values[0][4]
        #             }
        #         }
        #         actions.append(action)
        #
        # # 分批提交es数据
        # l = 0
        # r = 5000
        # length = len(actions)
        # while (l < length):
        #     helpers.bulk(es, actions[l:r])
        #     l += 5000
        #     r += 5000

    finally:
        print('mongo资源释放')

if __name__ == '__main__':
    mongo_output()
