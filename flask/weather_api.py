from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def weather():
    url = "https://www.weather.com.cn/weather1d/101280101.shtml#search"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36 Edg/93.0.961.52"
    }

    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, 'lxml')

    clearfix = soup.find_all('ul', class_="clearfix")
    weather_info = clearfix[1]

    h1 = weather_info.find_all('h1')
    tem = weather_info.find_all('p', class_="tem")
    wea = weather_info.find_all('p', class_="wea")

    gz_weather = {
        "daytime": h1[0].text,
        "daytime_tem": tem[0].text.replace('\n', ''),
        "daytime_wea": wea[0].text,
        "nighttime": h1[1].text,
        "nighttime_tem": tem[1].text.replace('\n', ''),
        "nighttime_wea": wea[1].text,
    }

    response = jsonify(gz_weather)  # 自动序列化，ensure_ascii=False生效
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # 指定编码[1,3](@ref)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8088,debug=True)




