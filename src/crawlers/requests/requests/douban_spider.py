#coding=utf-8
#爬取豆瓣电影TOP250

import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

#定义页面与请求头信息
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
}

def get_page_info(url):
    #获取页面数据
    resp = requests.get(url,headers=headers).text
    #print(resp)

    #解析数据
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                     r'</span>.*?<div class="bd">.*?<br>(?P<year>.*?)'
                     r'&nbsp;/&nbsp;(?P<country>.*?)&nbsp;/&nbsp;(?P<mtype>.*?)'
                     r'</p>.*?<div class="star">.*?<span class="rating_num" property="v:average">(?P<rat>.*?)'
                     r'</span>.*?<span>(?P<number>.*?)人评价</span>', re.S)

    results = obj.finditer(resp)


    for result in results:
        # 打印方式一
        print(result.group("year").strip(), result.group("name"), result.group("rat"), result.group("number"))

        # 转化为字典格式
        dic = result.groupdict()
        dic['year'] = dic['year'].strip()
        dic['mtype'] = dic['mtype'].strip()

        # 打印方式二


        # print(dic.values())

        # 打印方式三
        # for key in dic.keys():
        #     print(key,":",dic.get(key))
        # print("-------------------------")

        # 将字典数据写入excel文件
        # with open('douban_top.csv', 'a') as f:
        #     csvwrite=csv.writer(f) #定义csv写人
        #     csvwrite.writerow(dic.values())

# 爬取豆瓣10页电影信息
for i in range(10):
    page = i * 25
    url = f'https://movie.douban.com/top250?start={page}&filter='
    # print (url)
    # print (f"第{i}页")
    get_page_info(url)

# with ThreadPoolExecutor(10) as t:
#    for i in range(10):
#         page = i * 25
#         url = f'https://movie.douban.com/top250?start={page}&filter='
#         t.submit(get_page_info, url=url)
