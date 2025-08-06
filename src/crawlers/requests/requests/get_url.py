from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import html


def extract_content_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style", "meta", "link", "head"]):
        script.decompose()
    text = soup.get_text(separator='\n', strip=True)
    text = html.unescape(text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def get_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62"
    }

    session = HTMLSession()
    r = session.get(url=url, headers=headers)
    html = r.content.decode('utf-8')

    data = extract_content_from_html(html)
    return data


url_list = [
    "https://www.sohu.com/a/885155106_639898",
    ]

content_list = []

if __name__ == '__main__':
    for url in url_list:
        data_list = get_info(url)
        content_list.append(data_list)
    print(content_list)










