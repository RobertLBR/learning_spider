from requests_html import HTMLSession
import re

session = HTMLSession()

url = 'https://baike.baidu.com/item/mini'

r = session.get(url)
html = r.content.decode('utf-8')

data = re.findall(f'content="(.*?)"',html,re.DOTALL)
print(data)
