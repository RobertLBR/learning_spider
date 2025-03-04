import requests

# 定义要翻译的文本
text = 'Hello, world!'

# 定义表单数据
data = {
    'q': text,
    'from': 'en',
    'to': 'zh-CN'
}

# 发送POST请求
response = requests.post('https://api.youdao.com/translate', data=data)

# 解析HTTP POST请求的响应
result = response.json()

# 获取翻译结果
translation = result['trans_result'][0]['dst']

# 打印翻译结果
print(translation)
