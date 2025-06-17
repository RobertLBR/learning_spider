from flask import Flask, request
from requests_html import HTMLSession
import re
import json

app = Flask(__name__)

def get_content(url):

    # 创建HTML会话对象
    session = HTMLSession()

    # 发送GET请求获取网页内容
    r = session.get(url)

    # 将网页内容转换成UTF-8的格式
    html = r.content.decode('utf-8')

    # 使用正则表达式查找所有meta标签的content属性值
    # 正则表达式说明: content="(.*?)": 匹配content属性值，使用非贪婪模式
    pattern = f'content="(.*?)"'
    data = re.findall(pattern ,html ,re.DOTALL)
    return data

@app.route('/get_content', methods=['GET'])
def handle_get_content():

    # 传入URL参数
    url_param = request.args.get('url')

    if not url_param:
        return json.dumps({'error': '缺少URL参数'}, ensure_ascii=False), 400, {
            'Content-Type': 'application/json; charset=utf-8'}

    try:
    # 获取页面内容，成功返回200
        content = get_content(url_param)
        return json.dumps({'content': content}, ensure_ascii=False), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    # 捕捉异常返回500
    except Exception as e:
        return json.dumps({'error': str(e)}, ensure_ascii=False), 500, {
            'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888)

# 请求
# curl -X GET "http://172.16.100.119:18888/get_content?url=https://baike.baidu.com/item/mini"