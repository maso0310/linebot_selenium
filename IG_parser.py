from selenium import webdriver
from bs4 import BeautifulSoup
from linebot.models import *

def IG_imagemap_maker(url):
    driver = webdriver.Chrome()
    driver.get(url)
    image_list = driver.find_elements_by_class_name('FFVAD')
    print(image_list)

    contents = {}
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
                                "aspectRatio": "20:13",
                                "aspectMode": "cover",
                                "action": {
                                "type": "uri",
                                "uri": image_url
                                }
                            }
                        }
            contents['contents'].append(bubble)
            i+=1
    
    message = FlexSendMessage(alt_text='IG照片瀏覽',contents=contents)
    return message

    
    
#可於本機中直接執行python IG_parser.py進行單元測試
if __name__=='__main__':
    IG_imagemap_maker('https://instagram.com/mybosseatshit?utm_medium=copy_link')