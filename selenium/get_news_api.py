from flask import Flask, request
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import html
import json

app = Flask(__name__)


def extract_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style", "meta", "link", "head"]):
        script.decompose()
    text = soup.get_text(separator='\n', strip=True)
    text = html.unescape(text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def get_content(url):
    remote_url = "http://172.16.101.252:4444/wd/hub"
    # remote_url = "http://172.16.0.3:4444/wd/hub"
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")  # 显式启用（部分环境需要）
    options.add_argument("--disable-web-security")  # 关闭同源策略限制[8](@ref)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    try:
        driver.get(url)
        driver.implicitly_wait(10)
        return extract_content_from_html(driver.page_source)
    finally:
        driver.quit()


@app.route('/get_content', methods=['GET'])
def handle_get_content():
    url_param = request.args.get('url')
    if not url_param:
        return json.dumps({'error': '缺少URL参数'}, ensure_ascii=False), 400, {
            'Content-Type': 'application/json; charset=utf-8'}

    try:
        content = get_content(url_param)
        return json.dumps({'content': content}, ensure_ascii=False), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False), 500, {
            'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888)

# 请求
# curl -X GET "http://172.16.100.119:18888/get_content?url=https://baike.baidu.com/item/mini"