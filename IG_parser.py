from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from linebot.models import *
import time
import os
import random

def youtube_vedio_parser(keyword):
    url = 'https://tw.youtube.com/'
    driver = webdriver.Chrome()
    driver.get(url)
    search_vedio = driver.find_element_by_name('search_query')
    search_vedio.send_keys(keyword)
    search_vedio.send_keys(Keys.RETURN)
    search_button = driver.find_element_by_id('search-icon-legacy')
    search_button.click()
    time.sleep(3)

    image_path = './static/tmp/test.png'
    if os.path.isfile(image_path)==True:
        os.remove(image_path)
    driver.save_screenshot(image_path)
    
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