from flask import Flask, request
from requests_html import HTMLSession
import re
import json

app = Flask(__name__)

def get_content(url):
    session = HTMLSession()
    url = url
    r = session.get(url)
    html = r.content.decode('utf-8')

    data = re.findall(f'content="(.*?)"', html, re.DOTALL)
    return data

@app.route('/get_content', methods=['GET'])
def handle_get_content():
    url_param = request.args.get('url')
    # content = get_content(url_param)
    # return json.dumps({'content': content})

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