# 下载防盗链视频
# 1、拼接出原视频URL
# 2、获取contID
# 3、找到videoStatus获取srcUrl
# 4、下载视频

import requests
from lxml import etree

def download_video(url):
    # 获取内容ID
    contID = url.split("_")[1]

    # 拼接视频状态连接
    videoStatus = f"https://www.pearvideo.com/videoStatus.jsp?contId={contID}&mrd=0.8490507236476952"

    # 增加防盗链参数
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62" ,
        "Referer": url
    }

    # 获取到videoStatus页面中的json信息
    result_json = requests.get(videoStatus, headers=headers).json()

    # 提取出systemTime和srcUrl
    systemTime = result_json['systemTime']
    srcUrl = result_json['videoInfo']['videos']['srcUrl']

    # 拼接出真正的视频连接
    videoURL = srcUrl.replace(systemTime, f"cont-{contID}")

    # 获取视频内容
    video_content = requests.get(videoURL).content

    # 下载视频到指定路径中
    with open(fr"D:\IT\Python\output\video\{contID}.mp4", "wb") as f:
        f.write(video_content)

# 主函数
def main():
    domain_url = "https://www.pearvideo.com/"
    url = "https://www.pearvideo.com/category_130"

    # 获取页面html源码
    html = requests.get(url).text

    # xpath表达式解析
    tree = etree.HTML(html)
    video_id_list = tree.xpath('//*[@id="categoryList"]/li/div/a/@href')
    video_title_list = tree.xpath('//*[@id="categoryList"]/li/div/a/div[2]/text()')

    for i in range(len(video_id_list)):
        # 拼接视频页面URL
        video_url = domain_url + video_id_list[i]
        # 提取视频名称
        video_title = video_title_list[i]
        print(video_title, video_url)

        # 开始下载视频
        download_video(video_url)

if __name__ == '__main__':
    main()

