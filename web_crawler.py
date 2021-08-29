from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from linebot.models import *
from flex_msg import *
from config import *
import time
import os
import random
import string
import re

def youtube_vedio_parser(keyword):
    #建立url跟目錄
    url = 'https://tw.youtube.com/'
    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    #設定瀏覽器的語言為utf-8中文
    chromeOption.add_argument("--lang=zh-CN")
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


    #在static資料夾中建立一個暫存圖片路徑
    image_path = './static/tmp/test.png'
    #若目前已經有圖片則將其圖片刪除
#    if os.path.isfile(image_path)==True:
#        os.remove(image_path)
    #將目前的頁面截圖儲存至暫存圖片路徑
    driver.refresh()
    driver.save_screenshot(image_path)

    time.sleep(5)

    #建立影片url列表
    vedio_url_list = []
    #以css選擇器搜尋youtube的影片連結    
    yt_vedio_urls = driver.find_elements_by_css_selector('.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail')
    #將每個影片連結放入連結list
    print(len(yt_vedio_urls))
    for url in yt_vedio_urls:
        print(url.get_attribute('href'))
        if len(vedio_url_list)<10:
            vedio_url_list.append(url.get_attribute('href'))

    
    #滾動視窗捲軸，使瀏覽器獲取影片縮圖資訊
    for i in range(50):
        y_position = i*100
        driver.execute_script(f'window.scrollTo(0, {y_position});')
        time.sleep(0.1)
    
    #建立縮圖列表
    yt_vedio_images = []
    yt_vedio_images_urls = driver.find_elements_by_css_selector('.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail yt-img-shadow img#img')

    #將每個圖片的縮圖放入圖片list
    for image in yt_vedio_images_urls:
        print(type(image.get_attribute('src')))
        if str(type(image.get_attribute('src'))) != "<class 'NoneType'>":
            if 'ytimg' in image.get_attribute('src') or '720.jpg?' in image.get_attribute('src') or 'hqdefault.jpg?' in image.get_attribute('src'):
                print(image.get_attribute('src'))
                if len(yt_vedio_images)<10:
                    yt_vedio_images.append(image.get_attribute('src'))
    
    #建立標題列表
    yt_title_list = []
    yt_vedio_infos = driver.find_elements_by_css_selector('#video-title')
    print(len(yt_vedio_infos))
    for infos in yt_vedio_infos:
        print(infos.get_attribute('title'))
        yt_title_list.append(infos.get_attribute('title'))

    #建立頻道資訊列表(圖片)
    yt_channel_infos_image_urls = []
    yt_channel_infos_image_list = driver.find_elements_by_css_selector('#channel-info a yt-img-shadow #img')
    for infos in yt_channel_infos_image_list:
        print(infos.get_attribute('src'))
        yt_channel_infos_image_urls.append(infos.get_attribute('src'))

    #建立頻道資訊列表(頻道名稱)
    yt_channel_infos_names = []
    yt_channel_infos_name_list = driver.find_elements_by_css_selector('#channel-info ytd-channel-name div#container div#text-container yt-formatted-string a')
    for infos in yt_channel_infos_name_list:
        yt_channel_infos_names.append(infos.text)
#        print(infos.text)
#        print(infos.get_attribute('src'))
#        yt_channel_infos_names.append(infos.get_attribute('src'))
    
    
    import csv
    with open('./yt.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['vedio_url','image_url'])

    for vedio_url, image_url in zip(vedio_url_list,yt_vedio_images):

        with open('./yt.csv','a',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([vedio_url,image_url])

    print(yt_vedio_images)
    print(len(yt_vedio_images))

    message = []    
    #建立一個隨機4碼的字串，使圖片縮圖瀏覽不會因為讀取同一個url快取而重覆
    random_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
    message.append(ImageSendMessage(original_content_url=heroku_APP_url + '/static/tmp/test.png?'+random_code,preview_image_url='https://hjuav.herokuapp.com/static/tmp/test.png?'+random_code))

    #回傳搜尋結果的FlexMessage
    message.append(image_carousel('YT搜尋結果',yt_vedio_images,vedio_url_list,yt_title_list,yt_channel_infos_image_urls,yt_channel_infos_names))

    return message
   
    
#可於本機中直接執行python web_crawler.py進行單元測試
if __name__=='__main__':
    youtube_vedio_parser('Maso的萬事屋')