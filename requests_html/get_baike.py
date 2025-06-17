from requests_html import HTMLSession
import re

session = HTMLSession()

url = 'https://www.autohome.com.cn/7979'

r = session.get(url)
html = r.content.decode('utf-8')

data = re.findall(f'content="(.*?)"',html,re.DOTALL)
print(data)
