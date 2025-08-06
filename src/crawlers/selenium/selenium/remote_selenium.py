from selenium import webdriver

# 配置远程 WebDriver 连接
remote_url = "http://172.16.101.252:4444/wd/hub"  # 确保URL包含/wd/hub后缀

# 使用 Chrome 浏览器配置（可根据服务器支持的浏览器修改）
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 不显示图形界面
options.add_argument("--no-sandbox")  # 绕过OS安全模型

# 创建远程 WebDriver 实例
driver = webdriver.Remote(
    command_executor=remote_url,
    options=options
)

try:
    # 访问网址
    driver.get('https://baike.baidu.com/item/mini')

    # 等待页面加载（可根据需要调整等待时间）
    driver.implicitly_wait(10)

    # 获取页面源码
    print(driver.page_source)

finally:
    # 关闭浏览器
    driver.quit()
