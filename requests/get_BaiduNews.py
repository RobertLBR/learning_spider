# coding=utf8
# 爬取百度新闻
import requests
from lxml import etree

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
url = "http://news.baidu.com/tech"

# 使用代理IP
# proxies = {
#     "https": "https:172.16.100.50:3128"
# }

# data = requests.get(url=url, headers=headers, proxies=proxies).content
data = requests.get(url=url, headers=headers).content
html = etree.HTML(data)

# xpath表达式取出title，class="ulist fb-list"的ul标签下，target="_blank"的a标签里的文字内容
titles_list = html.xpath('//ul[@class="ulist fb-list"]/li/a[@target="_blank"]')

# xpath表达式取出link的信息，class="ulist fb-list"的ul标签下，target="_blank"的a标签里的href属性内容
links_list = html.xpath('//ul[@class="ulist fb-list"]/li/a[@target="_blank"]/@href')

for a in range(len(titles_list)):
    title = titles_list[a]
    links = links_list[a]
    print(title.text + ":" + links)

