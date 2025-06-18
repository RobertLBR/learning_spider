# 采集中关村新出的手机型号

import requests
from bs4 import BeautifulSoup

# 模拟浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
}

input_url = "https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1_s11066_9_1_0_1.html"

# 发起 GET 请求获取网页
response = requests.get(url=input_url, headers=headers)

# 解析为 LXML 格式的 BeautifulSoup 对象
soup = BeautifulSoup(response.text, 'lxml')

# 找到所有商品容器
# 源码 <div class="list-item item-one clearfix" data-follow-id="p2128352">
tag_div_list = soup.find_all('div', class_="list-item clearfix")

cnt = 0
for tag_div in tag_div_list:
    # 商品名称：从 <h3> 中的 <a> 标签提取
    # 源码 <h3><a href="/cell_phone/index2128352.shtml" target="_blank">vivo S30(12GB/256GB)</a></h3>
    product_name = tag_div.find('h3').find('a').text

    # 商品价格：从 class_='price-type' 的 b 标签中提取
    # 源码 <b class="price-type">2699</b>
    price = tag_div.find('b', class_='price-type').text

    # 发售时间：从 class_='date' 的 span 标签中提取
    # 源码 <span class="date">2025-06-10</span>
    sale_date = tag_div.find('span', class_='date').text

    cnt += 1
    print(f"{cnt}.日期：{sale_date} 型号：{product_name} 售价：{price}")

