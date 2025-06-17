# 查看今日头条的网页信息
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置浏览器选项
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # 启用新版无头模式，不显示浏览器界面
options.add_argument("--enable-javascript")  # 确保启用JavaScript（默认已启用，显式声明明确意图）
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")  # 设置用户代理，模拟真实浏览器
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 隐藏自动化控制提示
options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用Blink的自动化控制特性

# 配置远程WebDriver连接地址（通常是Selenium Grid或Docker容器地址）
remote_url = "http://172.16.101.252:4444/wd/hub"  # 注意必须包含/wd/hub后缀
# remote_url = "https://dev:31uKJdwoyvVjSTBD@ai.guide-rank.com:14444/wd/hub"

# 初始化远程WebDriver（支持分布式测试）
driver = webdriver.Remote(
    command_executor=remote_url,
    options=options  # 传入配置好的浏览器选项
)

try:
    # 访问目标网页
    driver.get("https://www.toutiao.com/article/7496698159268168218")

    # 使用显式等待确保内容加载完成（最多等待30秒）
    # 等待直到找到指定CSS选择器的元素（文章内容区域）
    content_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".article-content"))
    )

    # 输出渲染后的文本内容
    print(content_element.text)
finally:
    # 确保无论是否发生异常都会关闭浏览器
    driver.quit()