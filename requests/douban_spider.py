#coding=utf-8
#爬取豆瓣电影TOP250

import requests
import re
from bs4 import BeautifulSoup

# 获取页面源码
def get_page_info(url):
    # 定义页面与请求头信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
    }

    #获取页面数据
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    resp = res.text
    return resp


# 使用BeautifulSoup提取页面内容
def soup_data(resp):
    soup = BeautifulSoup(resp,'lxml')
    items = soup.find_all('div',class_="item")

    for item in items:
        try:
            # soup提取
            rank = item.find('em').text
            title = item.find('span',class_="title").text
            average = item.find('span',class_="rating_num").text
            info = item.find('p').text.replace('\n','').replace(' ','')
            print("排名：",rank,"评分：",average,"电影：",title,"年份：",info.split("...")[1])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 爬取豆瓣10页电影信息
    for i in range(10):
        page = i * 25
        url = f'https://movie.douban.com/top250?start={page}&filter='
        print (f"第{i+1}页")

        # 获取页面源码
        resp = get_page_info(url)

        # 使用BS4处理
        soup_data(resp)

        # 测试
        # break