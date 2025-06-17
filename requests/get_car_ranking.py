import requests
import json

# 请求头
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://editor.guiderank-app.com"
}

# 获取榜单ID
def get_rid(headers):
    url = "https://editor.guiderank-app.com/guiderank-editor/admin/car/getCarRankings?token=3iSNWL4S31v6cmBTvMHRKfVU"

    payload = {
        "firstCategoryId":"",
        "secondCategoryId":"",
        "name":""
    }

    res = requests.post(url=url ,headers=headers ,json=payload)
    json_data = json.loads(res.content)
    id_dict = dict(json_data)

    rid_list = []
    for rid in id_dict['data']['rankings']:
        rid_list.append(rid['rankingId'])
    # print(rid_list)
    return rid_list

# 获取榜单内容
def get_ranking(headers,rid):
    url = "https://editor.guiderank-app.com/guiderank-editor/admin/car/getCarRankingGlobals?token=3iSNWL4S31v6cmBTvMHRKfVU"
    payload = { "rankingId": rid}
    res = requests.post(url=url ,headers=headers ,json=payload)
    json_data = json.loads(res.content.decode('utf-8'))
    car_dict = dict(json_data)
    cat_list = []
    for i in car_dict['data']['globals']:
        cat_list.append(i['carSeriesName'])
    return cat_list


def get_car_info():
    rid_list = get_rid(headers)
    result_list = []
    for rid in rid_list:
        cat_list = get_ranking(headers,rid)
        for car in cat_list:
            result_list.append(car)
    result = list(set(result_list))
    print(result)
    return result

if __name__=='__main__':
    get_car_info()