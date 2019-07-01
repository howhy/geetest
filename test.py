# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time, random
import requests,json
import traceback

def solid_vad(driver):
    driver.save_screenshot('printscreen.png')
    back_url = driver.find_element_by_class_name("geetest_slicebg ")##定位到验证码背景图片
    location = back_url.location  # 获取验证码背景图片x,y轴坐标
    size = back_url.size  # 获取验证码背景图片的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 我们需要截取验证码背景图片坐标
    i = Image.open("printscreen.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('back_img.png')
    time.sleep(1)
    upurl="http://182.61.37.17/api/imgvalid" ##系统接口
    data={"appkey":"463eb7dd8c0d450e89c02dfa2ea816f5","appsecert":"ecc5ec79b25a4627b78c06c8d3495cef"}
    files={'file': ('small.png', open('back_img.png', 'rb'),"image/jpeg")}
    ret=requests.post(upurl,data=data,files=files).json()
    print(ret)
    track_list = ret["locationArr"]
    element = driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')##定位到滑动圆球
    location = element.location
    # 获得滑动圆球的高度
    y = location["y"]
    # 鼠标点击元素并按住不放
    ActionChains(driver).click_and_hold(on_element=element).perform()
    for track in track_list:
        ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 32,yoffset=y - 445).perform()
        # 间隔时间也通过随机函数来获得,间隔不能太快,否则会被认为是程序执行
        time.sleep(random.randint(10, 50) / 100)
    # 释放鼠标
    ActionChains(driver).release(on_element=element).perform()

def main(username,password,kw):
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')  # 显示自动化--auto-open-devtools-for-tabs
        option.add_argument('start-maximized')
        driver = webdriver.Chrome(executable_path="C:\\Python27\\\chromedriver_win32\\chromedriver.exe",chrome_options=option)
        driver.get("https://passport.bilibili.com/login")
        time.sleep(1)
        driver.find_element_by_id("login-username").send_keys(username)##bili账号
        driver.find_element_by_id("login-passwd").send_keys(password)##bili密码
        driver.find_element_by_class_name("btn-login").click()
        time.sleep(1)
        solid_vad(driver)
        time.sleep(2)
        driver.find_element_by_class_name("search-keyword").send_keys(kw)
        driver.find_element_by_class_name('search-submit').click()
        time.sleep(3)
        driver.quit()
    except Exception as e:
        print(e)
        traceback.print_exc()
        driver.quit()
if __name__=="__main__":
    for a in range(10):
        main("bilibili账号","bilibili密码","python")