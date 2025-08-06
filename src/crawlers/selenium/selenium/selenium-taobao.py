# 导入selenium
import time
from selenium import webdriver
from lxml import etree

def get_taobao_data(data,select_keyword):
    # 使用xpath格式化数据与清洗数据
    html = etree.HTML(data)
    title_list = html.xpath('//img[@class="J_ItemPic img"]/@alt')
    shop_list = html.xpath('//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]')
    price_list = html.xpath('//div[@class="price g_price g_price-highlight"]/strong')
    cnt_list = html.xpath('//div[@class="deal-cnt"]')
    url_list = html.xpath('//div[@class="row row-2 title"]/a/@href')
    file_name = str(select_keyword) + ".csv"

    for i in range(len(title_list)):
        try:
            print ("product_name: " + title_list[i])
            print ("shop_name   : " + shop_list[i].text)
            print ("price       : " + price_list[i].text)
            print ("cnt         : " + cnt_list[i].text)
            print ("url         : " + url_list[i].text)
            print ("\n")
            result = title_list[i] + "," + shop_list[i].text + "," + price_list[i].text + "," + cnt_list[i].text
            with open(f'./taobao/{file_name}', 'a') as f:
                f.write(result + "\n")
        except:
            print ("error-----------------:" + str(i))


def main(select_keyword):
    # 加载谷歌浏览器驱动
    driver = webdriver.Chrome(executable_path="D:\IT\Python\chromedriver_win32\chromedriver.exe")
    # 在浏览器找不到元素时继续等待，隐式等待超时限制60秒
    driver.implicitly_wait(60)

    # 输入网址
    driver.get("https://www.taobao.com/")

    # 点击登录按钮，使用扫码登录
    driver.find_element_by_class_name("h").click()
    driver.find_element_by_xpath('//i[@class="iconfont icon-qrcode"]').click()

    print("请在浏览器上扫码登录……")

    # 输入搜索关键字
    driver.find_element_by_xpath('//input[@role="combobox"]').send_keys(select_keyword)

    # 点击搜索
    driver.find_element_by_xpath('//button[@class="btn-search tb-bg"]').click()
    time.sleep(3)

    # 获取页面代码
    data = driver.page_source

    # 提取网页数据
    get_taobao_data(data, select_keyword)

    # 打印出多页数据
    for i in range(3):
        # 翻页
        driver.find_element_by_xpath('//span[@class="icon icon-btn-next-2"]').click()
        time.sleep(3)
        # 获取下一页代码
        data = driver.page_source
        # 提取下一页数据
        get_taobao_data(data, select_keyword)



if __name__ == '__main__':
    select_keyword = "智能开关"
    main(select_keyword)

