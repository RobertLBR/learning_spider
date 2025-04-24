from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def configure_browser():
    """针对动态类名优化的浏览器配置"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")  # 避免响应式布局
    options.add_argument("--log-level=3")  # 禁用控制台日志
    return options


def parse_car_items(driver):
    """基于页面结构特征的新型解析方法"""
    # 等待列表容器加载
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.content.fl"))
    )

    car_list = []
    # 定位所有车型卡片容器
    items = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/auto/series/"] > div.list.clearfix')

    for item in items:
        try:
            # 通过相对定位获取数据
            car_data = {
                "车型名称": item.find_element(By.CSS_SELECTOR, "div.series.fl.clearfix > p:nth-child(2)").text,
                "价格区间": item.find_element(By.CSS_SELECTOR, "div.series.fl.clearfix > p:last-child").text,
                "上市时间": item.find_element(By.CSS_SELECTOR, "div.series.fl.clearfix > p:first-child").text,
                "详情链接": item.find_element(By.XPATH, './..').get_attribute("href"),
                "封面图":
                    item.find_element(By.CSS_SELECTOR, "div.cover.fl").value_of_css_property("background-image").split(
                        '"')[1]
            }
            car_list.append(car_data)
        except Exception as e:
            print(f"部分数据解析失败: {str(e)}")
    return car_list


def fetch_dongchedi():
    driver = webdriver.Remote(
        command_executor="http://172.16.101.252:4444/wd/hub",
        options=configure_browser()
    )

    try:
        driver.get("https://www.dongchedi.com/newcar")

        # 初始化CSV文件
        with open('../cars_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ["车型名称", "价格区间", "上市时间", "详情链接", "封面图"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            page = 5
            while True:
                print(f"正在采集第 {page} 页...")
                current_cars = parse_car_items(driver)

                # 写入数据
                writer.writerows(current_cars)

                # 智能分页(根据实际分页元素调整)
                try:
                    next_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "p.more"))
                    )
                    next_btn.click()
                    WebDriverWait(driver, 15).until(EC.staleness_of(current_cars[0]))
                    page += 1
                except Exception as e:
                    print(f"分页结束: {str(e)}")
                    break

    finally:
        driver.quit()


if __name__ == "__main__":
    fetch_dongchedi()