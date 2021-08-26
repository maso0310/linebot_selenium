from selenium import webdriver
from bs4 import BeautifulSoup

def IG_imagemap_maker(url):
    driver = webdriver.Chrome()
    driver.get(url)
    image_list = driver.find_elements_by_class_name('FFVAD')
    print(image_list)