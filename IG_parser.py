from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from linebot.models import *
import time
import os
import random

def youtube_vedio_parser(keyword):
    #建立url跟目錄
    url = 'https://tw.youtube.com/'
    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    chromeOption.add_argument("--lang=zh-CN.UTF-8")
    #開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    #進入指定網址
    driver.get(url)
    #定義一個物件，以name標籤找到youtube的關鍵字搜尋欄位
    search_vedio = driver.find_element_by_name('search_query')
    #將關鍵字文字送入搜尋欄位
    search_vedio.send_keys(keyword)
    #按下輸入搜尋按鈕
#    search_vedio.send_keys(Keys.RETURN)
    search_button = driver.find_element_by_id('search-icon-legacy')
    search_button.click()
    #等待網頁讀取
    time.sleep(5)

    #在static資料夾中建立一個暫存圖片路徑
    image_path = './static/tmp/test.png'
    #若目前已經有圖片則將其圖片刪除
#    if os.path.isfile(image_path)==True:
#        os.remove(image_path)
    #將目前的頁面截圖儲存至暫存圖片路徑
    driver.save_screenshot(image_path)
    
    #以css選擇器搜尋youtube的影片縮圖    
    yt_vedio_images = driver.find_elements_by_css_selector('img#img.style-scope.yt-img-shadow')
    print(yt_vedio_images)
    #將每個圖片的縮圖放入圖片list
    for image in yt_vedio_images:
        print(image.get_attribute('src'))

    #以css選擇器搜尋youtube的影片連結    
    yt_vedio_urls = driver.find_elements_by_css_selector('.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail')
    print(yt_vedio_urls)
    #將每個影片連結放入連結list
    for url in yt_vedio_urls:
        if 'ytimg' in url.get_attribute('href'):
            print(url.get_attribute('href'))

        
    return ImageSendMessage(original_content_url='https://hjuav.herokuapp.com/static/tmp/test.png?',preview_image_url='https://hjuav.herokuapp.com/static/tmp/test.png?')

'''
time.sleep(5)  

user_name = driver.find_element_by_name('username')
user_name.send_keys('masoufo0310@gmail.com')
password = driver.find_element_by_name('password')
password.send_keys('2626ioxaagu')
password.send_keys(Keys.RETURN)

time.sleep(5)  

check_save_info = driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF')
check_save_info.click()
image_list = driver.find_elements_by_class_name('FFVAD')
print(image_list)

driver.get(url)

contents = dict()
contents['type'] = 'carousel'
contents['contents'] = []
i=0
for image in image_list:
    if i<=10:
        print(image.get_attribute('src'))
        image_url = image.get_attribute('src')
        bubble =    {  "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": image_url,
                            "size": "full",
                            "aspectRatio": "1:1",
                            "aspectMode": "cover",
                            "action": {
                            "type": "uri",
                            "uri": image_url
                            }
                        }
                    }
        contents['contents'].append(bubble)
        i+=1
print(contents)
message = FlexSendMessage(alt_text='IG照片瀏覽',contents=contents)
return message
'''
    
    
#可於本機中直接執行python IG_parser.py進行單元測試
if __name__=='__main__':
    IG_imagemap_maker('https://instagram.com/mybosseatshit?utm_medium=copy_link')