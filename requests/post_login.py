#coding=utf-8
# 模拟登陆
import requests

# 会话
session = requests.session()
data = {
    "loginName": "13710706352",
    "password": "robert123"
}

# 登陆
url = "https://passport.17k.com/ck/user/login"
session.post(url, data=data)

# 在会话中获取登陆后的页面数据
info_url = "https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919"
resp = session.get(url=info_url)
print(resp.json())
