import requests
import json
from bs4 import BeautifulSoup
from  datetime import datetime

def scrape_new_cars():
    url = "https://www.dongchedi.com/newcar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    try:
        # 发送请求获取HTML
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取JSON数据
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if not script_tag:
            print("未找到JSON数据标签")
            return []

        # 解析JSON数据
        json_data = json.loads(script_tag.string)
        series_list = json_data.get("props", {}).get("pageProps", {}).get("series_list", [])

        cars = []
        for car in series_list:
            try:
                # 提取车型信息
                name = car.get("series_name", "未知车型")
                price_info = car.get("price_info", {})
                price = f"{price_info.get('price', '暂无报价')}{price_info.get('unit_text', '')}"

                # 组合发布日期（月/日）
                publish_date = f"{car.get('online_date_month', '?')}月{car.get('online_date_day', '?')}日"

                cars.append({
                    "name": name,
                    "price": price,
                    "publish_date": publish_date
                })
            except Exception as e:
                print(f"解析单条车型失败: {e}")

        return cars

    except Exception as e:
        print(f"爬取失败: {e}")
        return []


if __name__ == "__main__":
    cars = scrape_new_cars()
    # 数据统计
    day_str = datetime.now().strftime("%Y-%m-%d")

    print(f"截至至：{day_str} 新出车型数量：{len(cars)}")

    for car in cars:
        print(f"日期: {car['publish_date']} 车型：{car['name']} 售价: {car['price']}")