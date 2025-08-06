#coding=utf-8
#爬取百度贴吧图片
#xpath表达式的应用

#加载模块
import requests
from lxml import etree

#定义工具
class Spider(object):
    #定义初始化变量
    def __init__(self):
        self.tiebaName = "A股吧"
        self.beginPage = 1
        self.endPage = 5
        self.url = "http://tieba.baidu.com"
        self.ua_header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}
        self.filename = 1

    #构造一级页面URL
    def tiebaSpider(self):
        for page in range(self.beginPage,self.endPage+1):
            pn = ( page - 1 )*50
            myurl = str(self.url) + "/f?kw=" + str(self.tiebaName) + "&ie=utf-8&pn=" + str(pn)
            print("正在下载第" + str(page) + "页的图片=================")
            self.loadPage(myurl)

    #爬取一级页面，获取图片详情页
    def loadPage(self,url):
        data = requests.get(url=url, headers=self.ua_header).content
        html = etree.HTML(data)

        #获取class属性等于"threadlist_lz clearfix"的div标签下的二级div标签下的a标签下的href内容
        linklist = html.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')

        #排除删除没有图片的页面
        while '' in linklist:
            linklist.remove('')

        for links in linklist:
            links = self.url+links
            self.loadImages(links)

    #爬取二级页面，图片的链接
    def loadImages(self,link):
        data = requests.get(url=link,headers=self.ua_header).content
        html = etree.HTML(data)

        #获取class属性等于BDE_Image的img标签下的src内容
        imageslinks = html.xpath('//img[@class="BDE_Image"]/@src')

        for imageslink in imageslinks :
            self.writeImages(imageslink)

    #通过图片链接保持图片到本地
    def writeImages(self,imageslink):
        print('正在下载第' + str(self.filename) + '张' + str(self.tiebaName) + '的图片')

        #获取图片链接的数据
        data = requests.get(url=imageslink,headers=self.ua_header).content

        #将图片保存到本地
        file = open(r"D:\IT\Python\output\img\\" + str(self.tiebaName) + str(self.filename) + ".jpg", "wb")
        file.write(data)
        file.close()

        self.filename += 1

if __name__ == '__main__':
    mySpider = Spider()
    mySpider.tiebaSpider()



