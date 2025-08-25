"""
汽车排行榜数据抓取工具
该脚本通过API接口抓取汽车排行榜数据，提取榜单内所有车型名称
"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 常量定义
API_BASE_URL = "https://editor.guiderank-app.com/guiderank-editor/admin/car"
TOKEN = os.getenv('EDITOR_TOKEN')  # 从环境变量获取API令牌

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://editor.guiderank-app.com"
}

PARAMS = {"token": TOKEN}


def get_ranking_ids():
    """获取所有榜单ID"""
    # API端点设置
    endpoint = f"{API_BASE_URL}/getCarRankings"
    # 请求负载
    payload = {
        "firstCategoryId": "",
        "secondCategoryId": "",
        "name": ""
    }

    # 发送API请求
    response = requests.post(
        url=endpoint,
        headers=HEADERS,
        json=payload,
        params=PARAMS
    )

    # 验证响应状态
    response.raise_for_status()

    # 解析JSON响应
    data = response.json()

    # 提取所有榜单ID
    return [ranking['rankingId'] for ranking in data['data']['rankings']]


def get_cars_in_ranking(ranking_id):
    """获取指定榜单中的车型名称列表"""
    # API端点设置
    endpoint = f"{API_BASE_URL}/getCarRankingGlobals"
    # 请求负载
    payload = {"rankingId": ranking_id}

    # 发送API请求
    response = requests.post(
        url=endpoint,
        headers=HEADERS,
        json=payload,
        params=PARAMS
    )

    # 验证响应状态
    response.raise_for_status()

    # 解析JSON响应
    data = response.json()

    # 提取所有车型名称
    return [item['carSeriesName'] for item in data['data']['globals']]


def aggregate_car_data():
    """汇总所有榜单中的车型数据"""
    ranking_ids = get_ranking_ids()

    # 使用集合自动去重
    unique_cars = set()

    # 遍历每个榜单
    for rid in ranking_ids:
        try:
            car_models = get_cars_in_ranking(rid)
            unique_cars.update(car_models)
        except requests.exceptions.RequestException as e:
            print(f"榜单 {rid} 数据获取失败: {str(e)}")

    return sorted(list(unique_cars))  # 返回排序后的列表


if __name__ == '__main__':
    try:
        all_cars = aggregate_car_data()
        print("获取到的所有车型:")
        for idx, car in enumerate(all_cars, 1):
            print(f"{idx}. {car}")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")