# 集懂车帝新车上市列表
from requests_html import HTMLSession
import re
import json

session = HTMLSession()
url = 'https://www.dongchedi.com/newcar'

r = session.get(url)
html = r.content.decode('utf-8')

# 正则表达式取出新车列表
json_data_match = re.search(r'<script id="__NEXT_DATA__" type="application/json" crossorigin="anonymous">(.*?)</script>', html, re.DOTALL)
if json_data_match:
    json_data = json_data_match.group(1)
    data = json.loads(json_data)

    # 在列表中取出series_list的数据
    series_list = data['props']['pageProps']['series_list']

    # 在列表中取出需要的字段
    for series in series_list:
        series_name = series['series_name']
        price_info = series['price_info']['price']
        online_date_month = series['online_date_month']
        online_date_day = series['online_date_day']

        print(f"新车发布：{series_name}")
        print(f"售价范围：{price_info}")
        print(f"上市时间：{online_date_month}月{online_date_day}日")

        for tag in series['tag_list']:
            tag_type = tag['name']
            print(f"上新类型：{tag_type}")

        # 分割线
        print("-" * 20 )

else:
    print("JSON data not found in the HTML.")

