"""
使用代理采集人民电邮出版社的书单
"""
import requests
import json

url = 'https://www.ptpress.com.cn/bookinfo/getBookListForWS'

# 配置代理
proxy = {
    'http': '172.16.100.50:3128'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
}

return_data = requests.get(url, headers=headers, proxies=proxy).text
json_data = json.loads(return_data)
news = json_data['data']

for new in news:
    bookName = new['bookName']
    author = new['author']
    price = new['price']
    print("书名：", bookName, '\n', "作者：", author, '\n', "价格：", price, '\n')