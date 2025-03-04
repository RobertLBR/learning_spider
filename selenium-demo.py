# 导入selenium
import time
from selenium import webdriver

# 加载谷歌浏览器驱动
driver = webdriver.Chrome(executable_path="D:\IT\Python\chromedriver_win32\chromedriver.exe")

# 输入网址
driver.get("https://www.guide-rank.com/")

# 操作网址
time.sleep(5)

# 打印网页title
print(driver.title)

# 关闭浏览器
driver.quit()
