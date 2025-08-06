# 获取汽车之家的新车资讯
import requests
from bs4 import BeautifulSoup
from datetime import datetime

time_str = datetime.now().strftime('%Y-%m')
month_str = time_str.replace('-0', '-')

url = f"https://www.autohome.com.cn/newbrand/0-0-0-{month_str}.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# 取出所有a标签下class等于"pic placeholderimg scaleimg"的源码
tag_a = soup.find_all('a', class_="pic placeholderimg scaleimg")

dataList = []
for i in tag_a:
    # 取出tag_a的文字内容
    title = i.text.replace('\n', '')
    # 取出tag_a的href标签内容
    url = i['href']

    print(title, url)

    # 定义字典
    datadict = {"title": title, "url": url}

    # 装入列表，方便接口使用
    dataList.append(datadict)
