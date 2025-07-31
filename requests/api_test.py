import requests
import json

# 公共配置
headers = {
    "Authorization": "Bearer pat_67jA7gGJVaTfPPCG6v8303HtGh3wA6fG1Eml0PYDUqZ9ekuQVk8QNXY6EaNvn9dL",
    "Content-Type": "application/json"
}
base_url = "https://api.coze.cn/v1/workflow/run"


def call_workflow(workflow_id, parameters=None):
    """通用调用工作流函数"""
    payload = {
        "workflow_id": workflow_id
    }
    if parameters:
        payload["parameters"] = parameters

    response = requests.post(base_url, headers=headers, json=payload)
    result = response.json()

    # 处理嵌套的JSON字符串
    if 'data' in result:
        result['data'] = json.loads(result['data'])
        if 'data' in result['data']:
            result['data']['data'] = json.loads(result['data']['data'])

    return result


def get_latest_phones():
    """获取最新手机列表"""
    workflow_id = "7520067895263871026"
    return call_workflow(workflow_id)


def analyze_phone(product_name):
    """手机分析报告"""
    workflow_id = "7491517819621785639"
    parameters = {
        "product_name": product_name
    }
    return call_workflow(workflow_id, parameters)


def get_phone_ranking(product_name, category_id):
    """手机排名"""
    workflow_id = "7513792359400128538"
    parameters = {
        "product_name": product_name,
        "categoryId": category_id
    }
    return call_workflow(workflow_id, parameters)


# 示例调用
if __name__ == "__main__":
    # 1. 获取最新手机列表
    print("获取最新手机列表:")
    latest_phones = get_latest_phones()
    print(json.dumps(latest_phones, indent=2, ensure_ascii=False))

    # 2. 手机分析报告 (示例使用"努比亚红魔10S Pro")
    print("\n手机分析报告:")
    analysis = analyze_phone("努比亚红魔10S Pro")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

    # 3. 手机排名 (示例使用"努比亚红魔10S Pro"和指定categoryId)
    print("\n手机排名:")
    ranking = get_phone_ranking("努比亚红魔10S Pro", "15972230251503555196")
    print(json.dumps(ranking, indent=2, ensure_ascii=False))
