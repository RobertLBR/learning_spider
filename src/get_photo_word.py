#coding=utf-8
#通用文字提取
#需要先安装 pip install baidu-aip 的模块
from aip import AipOcr
import re
import importlib
import sys

#百度AI申请的文字识别API信息
APP_ID = "18552774"
API_KEY = "AGqUDVhME3jqdbOnrNWqQZDy"
SERCRET_KEY = "ZvoOM83upxZbcrZ0KuTRC1XFXr7M71j7"

#加载API信息
client = AipOcr(APP_ID,API_KEY,SERCRET_KEY)

#输入图片路径，转字符串
filepath = str(input("请输入图片所在的具体路径:"))

#以二进制的方式读取文字信息
with open(filepath, 'rb') as f:
    image = f.read()

#调用通用文字识别, 图片参数为本地图片
data = str(client.basicGeneral(image))

#正则表达式清洗数据
pat = re.compile(r"{u'words': u'(.*?)'}")
result_list = pat.findall(data)

#系统编码
importlib.reload(sys)

#循环获取列表所有数据
for result in result_list:
    # print(result)
    print(result.decode('unicode_escape'))
