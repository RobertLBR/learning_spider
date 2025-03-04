#coding=utf-8
#爬取淘宝商品信息

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
from lxml import etree

def get_taobao_data(data):

    #使用xpath格式化数据与清洗数据
    html = etree.HTML(data)
    title_list = html.xpath('//img[@class="J_ItemPic img"]/@alt')
    shop_list = html.xpath('//a[@class="shopname J_MouseEneterLeave J_ShopInfo"]/span[2]')
    price_list = html.xpath('//div[@class="price g_price g_price-highlight"]/strong')
    cnt_list = html.xpath('//div[@class="deal-cnt"]')

    for i in range(len(title_list)):
        try:
            print("product_name: " + title_list[i]      )
            print("shop_name   : " + shop_list[i].text  )
            print("price       : " + price_list[i].text )
            print("cnt         : " + cnt_list[i].text   )
            print("\n"                                  )
            result = title_list[i] + "," + shop_list[i].text + "," + price_list[i].text + "," + cnt_list[i].text
            with open("taobao.csv", 'a') as f:
                f.write(result + "\n")
        except:
            print("error-----------------:" + str(i))

# 淘宝信息爬取函数
def main(select):
    #定义浏览器参数
    s = Service(executable_path=r'D:\IT\Python\chromedriver_win32\chromedriver.exe')
    brower = webdriver.Chrome(service=s)
    brower.implicitly_wait(10)
    brower.get("https://www.taobao.com/")

    #点击登录
    login_button = brower.find_element(By.CLASS_NAME, "h")
    login_button.click()

    #等待页面加载
    brower.implicitly_wait(10)

    #输入账号密码
    user_name = brower.find_element(By.XPATH, '//input[@name="fm-login-id"]')
    user_name.send_keys("371539236@qq.com")

    user_pd = brower.find_element(By.XPATH, '//input[@name="fm-login-password"]')
    user_pd.send_keys("t86892825")

    # # 找到滑块
    # time.sleep(1)
    # user_button = brower.find_element(By.ID, "nc_1_n1z")
    #
    # # 拖动滑块
    # if __name__ == '__main__':
    #     move_to_gap(brower, user_button, get_track(340))

    # 手动拖到滑块后，点击登录
    time.sleep(5)
    brower.find_element(By.XPATH, '//button[@class="fm-button fm-submit password-login"]').click()

    # 导入系统编码格式
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    # select = u"羽毛球拍"

    #找到搜索框，并输入需要的文字
    brower.find_element(By.XPATH, '//input[@class="search-combobox-input"]').send_keys(select)

    #点击搜索
    brower.find_element(By.XPATH, '//button[@class="btn-search tb-bg"]').click()
    time.sleep(3)

    #获取页面代码
    data = brower.page_source

    #提取网页数据
    get_taobao_data(data)

    for i in range(5):
        #翻页
        brower.find_element(By.XPATH, '//span[@class="icon icon-btn-next-2"]').click()
        time.sleep(3)
        # 获取下一页代码
        data = brower.page_source
        # 提取下一页数据
        get_taobao_data(data)


#传入参数调用主函数
if __name__ == '__main__':
        # main(u"速干运动裤")
        main("aj")
