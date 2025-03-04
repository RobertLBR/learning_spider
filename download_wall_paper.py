#coding=utf-8
# 爬取高清壁纸
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 下载图片函数
def get_wall_paper(url):
    domian = "https://www.umei.cc"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
    }

    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"

    # 把源代码交给BeautifulSoup
    main_page = BeautifulSoup(resp.text, "html.parser")

    # 找出div标签class属性等于TypeList的a标签的内容
    alist = main_page.select('div[class="TypeList"] a')
    # alist = main_page.find("div", class_="TypeList").find_all("a") #第二种表达式，效果同上

    for a in alist:
        # 找到并拼接子页面地址
        url2 = domian + a.get('href')
        resp2 = requests.get(url2).text

        # 把源代码交给BeautifulSoup
        main_page2 = BeautifulSoup(resp2, "html.parser")
        # 找出div标签class属性等于ImageBody的p标签下的img标签的内容
        imglist = main_page2.select('div[class ="ImageBody"] p img')

        for img in imglist:
            # 找出图片地址
            img_url = img.get('src')
            img_name = img_url.split("/")[-1]
            img_content = requests.get(img_url).content
            print(f"开始下载{img_name}")
            #下载图片保存到本地
            with open(f"D:\Pictures\wall_paper\PC\{img_name}", "wb") as f:
                f.write(img_content)

# 使用进程池加快下载速度，开10个并发同时下载10页图片
with ThreadPoolExecutor(10) as t:
    for i in range(10):
        i = i + 1
        if i == 1:
            url = 'https://www.umei.cc/bizhitupian/fengjingbizhi'
        else:
            url = f'https://www.umei.cc/bizhitupian/fengjingbizhi/index_{i}.htm'
        print(f"进入第{i}页开始下载")
        t.submit(get_wall_paper, url=url)

