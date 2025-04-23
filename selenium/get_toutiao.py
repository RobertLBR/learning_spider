from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # 新版无头模式
options.add_argument("--enable-javascript")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--disable-blink-features=AutomationControlled")

# 配置远程 WebDriver 连接
remote_url = "http://172.16.101.252:4444/wd/hub"  # 确保URL包含/wd/hub后缀

driver = webdriver.Remote(
    command_executor=remote_url,
    options=options
)

try:
    driver.get("https://www.toutiao.com/article/7495991159136748044")
    content_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".article-content"))
    )
    print(content_element.text)  # 输出渲染后的文字页面
finally:
    driver.quit()