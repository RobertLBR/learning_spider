import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def get_baidu_search_results(query, max_results=10):
    # 设置请求头模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # 步骤1: 获取初始cookie（避免被百度反爬虫识别）
        with requests.Session() as session:
            # 访问百度首页获取初始cookie
            session.get('https://www.baidu.com', headers=headers, timeout=10)
            
            # 步骤2: 构造搜索URL
            search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
            
            # 步骤3: 发送搜索请求
            response = session.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()  # 检查请求是否成功
            
            # 步骤4: 解析搜索结果
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # 查找所有搜索结果项 - 根据百度页面结构调整选择器
            for item in soup.select('.result, .c-container, .result-op'):
                # 提取标题和链接
                title_tag = item.select_one('h3 a, .t a')
                if not title_tag:
                    continue
                    
                title = title_tag.get_text(strip=True)
                href = title_tag.get('href')
                
                # 跳过无效结果
                if not title or not href:
                    continue
                
                # 获取真实URL（处理百度重定向）
                try:
                    # 解析百度重定向链接获取真实URL
                    if href.startswith('http://www.baidu.com/link?url=') or href.startswith('/'):
                        # 获取重定向后的真实URL
                        redirect_response = session.head(
                            href if href.startswith('http') else f"https://www.baidu.com{href}",
                            headers=headers,
                            allow_redirects=True,
                            timeout=5
                        )
                        real_url = redirect_response.url
                    else:
                        real_url = href
                except:
                    real_url = href
                
                # 添加到结果列表
                results.append({
                    "title": title,
                    "url": real_url
                })
                
                # 达到最大结果数时停止
                if len(results) >= max_results:
                    break
            
            return results
    
    except Exception as e:
        print(f"百度搜索失败: {str(e)}")
        return []

if __name__ == '__main__':
    search_keyword = "site:www.autohome.com.cn 小米su7"
    results = get_baidu_search_results(search_keyword)
    
    print(f"获取到 {len(results)} 条搜索结果：")
    for i, item in enumerate(results, 1):
        print(f"{i}. [{item['title']}]({item['url']})")
        