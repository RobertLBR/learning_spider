# 调用spider接口获取数据
import requests

input_url = "https://baike.baidu.com/item/比亚迪汉"
url = f"https://dev:31uKJdwoyvVjSTBD@ai.guide-rank.com:18889/get_content?url={input_url}"

response = requests.get(url=url)
result = response.content.decode('utf-8')

print(result)

