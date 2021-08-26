from selenium import webdriver
from bs4 import BeautifulSoup

def IG_imagemap_maker(url):
    driver = webdriver.Chrome()
    driver.get(url)
    image_list = driver.find_elements_by_tag_name('img')
    print(image_list)
    return image_list