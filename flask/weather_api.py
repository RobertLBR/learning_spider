from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/")
def weather():
    url = "https://www.weather.com.cn/weather1d/101280101.shtml#search"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
    }

    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"

    # 格式化数据
    soup = BeautifulSoup(response.text, 'lxml')

    # 提取广州天气数据
    clearfix = soup.find_all('ul', class_="clearfix")
    weather_info = clearfix[1]

    # 提取广州天气指标
    h1 = weather_info.find_all('h1')
    tem = weather_info.find_all('p', class_="tem")
    wea = weather_info.find_all('p', class_="wea")

    # 把指标数据组装成字典
    gz_weather = {
        "daytime": h1[0].text,
        "daytime_tem": tem[0].text.replace('\n', ''),
        "daytime_wea": wea[0].text,
        "nighttime": h1[1].text,
        "nighttime_tem": tem[1].text.replace('\n', ''),
        "nighttime_wea": wea[1].text,
    }

    # 以JSON格式返回结果，防止中文乱码
    return (
        json.dumps(gz_weather, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'}
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081,debug=True)




