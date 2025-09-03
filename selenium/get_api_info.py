# 调用spider接口获取数据
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# 读取环境变量
USER = os.getenv("USER")
PWD = os.getenv("PWD")

input_url = "https://baike.baidu.com/item/比亚迪汉"
url = f"https://{USER}:{PWD}@ai.guide-rank.com:18889/get_content?url={input_url}"

response = requests.get(url=url)
result = response.content.decode('utf-8')

print(result)

