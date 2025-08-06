#coding=utf-8
#爬取天天基金网的基金

import requests

url = "http://fund.eastmoney.com/data/rankhandler.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
}

params = {
 "op": "ph",
 "dt": "kf",
 "ft": "all",
 "rs": "",
 "gs": "0",
 "sc": "6yzf",
 "st": "desc",
 "sd": "2021-12-29",
 "ed": "2022-12-05",
 "qdii": "",
 "tabSubtype": ",,,,,",
 "pi": "1",
 "pn": "50",
 "dx": "1",
 "v": "0.46465399774040983",
}

resp = requests.get(url, headers=headers, params=params)
print(resp.text)
