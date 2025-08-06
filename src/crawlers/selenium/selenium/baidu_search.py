from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def main(search_keyword):
    # 配置远程WebDriver
    remote_url = "http://172.16.101.252:4444/wd/hub"

    # 配置浏览器选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 避免被识别为自动化工具[3,8](@ref)

    try:
        # 初始化远程WebDriver
        driver = webdriver.Remote(
            command_executor=remote_url,
            options=chrome_options
        )

        # 打开百度
        driver.get("https://www.baidu.com")

        # 等待搜索框加载并输入关键词
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kw"))  # 使用ID定位搜索框[5,9](@ref)
        )
        search_box.send_keys(search_keyword)
        search_box.submit()  # 提交搜索[5](@ref)

        # 等待搜索结果加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#content_left .result"))  # 使用CSS选择器定位结果区域[2,10](@ref)
        )

        # 获取所有搜索结果链接
        results = driver.find_elements(By.CSS_SELECTOR, '#content_left .result h3 a')
        print(f"获取到 {len(results)} 条搜索结果：")

        # 提取并输出链接
        href_list = []
        for i, link in enumerate(results, 1):
            href = link.get_attribute('href')
            title = link.text
            # print(f"{i}. {title[:20]}... - {href}")
            url_dict = {
                "title":title,
                "url":href
            }
            href_list.append(url_dict)
        return href_list

    except Exception as e:
        print(f"执行过程中出错: {str(e)}")

    finally:
        # 确保关闭浏览器
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    search_keyword = "site:www.autohome.com.cn 小米su7"
    href_list = main(search_keyword)
    for i in href_list:
        print(i.values())
