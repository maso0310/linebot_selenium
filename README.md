# LINEBOT / Selenium / FlexMessaage  Youtube爬蟲

操作步驟：

1-1.下載範例程式碼，切換到範例檔案資料夾

```
git clone https://github.com/maso0310/linebot_selenium.git
cd linebot_selenium
```

1-2.如果要在本機進行selenium程式執行測試，需要根據本機的Chrome版本[下載chromedriver瀏覽器](https://chromedriver.chromium.org/)

2.在heroku設定chromedirver安裝環境，進入APP頁面後，從Settings中點選Add bulidpack，新增以下URL，在Heroku環境中安裝Google Chrome與ChromeDriver。設定完畢後將在下次程式部署Heroku時安裝，會使部署時間與變長，占用容量也會提高，因此會建議先在本機中以selenium爬蟲進行單元測試，確認效果後來再移植到LINEBOT上面。

```
https://github.com/heroku/heroku-buildpack-google-chrome
https://github.com/heroku/heroku-buildpack-chromedriver
```

![heroku settings](https://i.imgur.com/BXypZx0.jpg)

![heroku bulidpacks](https://i.imgur.com/SLgbH6K.jpg)

3.範例程式碼中更改config.py的 `CHANNEL_ACCESS_TOKEN`、`CHANNEL_SECRET`以及 `HEROKU_APP_URL`

4.將範例程式碼部署至Heroku App，在LINE Developer更改webhook url

5.LINEBOT試運行

# web_crawler.py  爬取Youtube影片資訊

程式運作流程：

1.開啟Chrome瀏覽器



```
    #開啟Chrome瀏覽器
    driver = webdriver.Chrome()
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)

```



2.進入youtube網頁並在搜尋欄位輸入關鍵字(keyword來自LINEBOT)



```
    #進入指定網址
    driver.get(url)
    #定義一個物件，以name標籤找到youtube的關鍵字搜尋欄位
    search_vedio = driver.find_element_by_name('search_query')
    #將關鍵字文字送入搜尋欄位
    search_vedio.send_keys(keyword)
    #按下輸入搜尋按鈕
    search_button = driver.find_element_by_id('search-icon-legacy')
    search_button.click()
```



3.進入瀏覽器之後截圖確認是否爬取正確的頁面


```
    #在static資料夾中建立一個暫存圖片路徑
    image_path = './static/tmp/test.png'
    #刷新網頁 => 移除原本youtube首頁的元素
    driver.refresh()
    #將目前的頁面截圖儲存至暫存圖片路徑
    driver.save_screenshot(image_path)

```



4.爬取影片url並且列表



```
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

```



5.使用driver.execute_script()執行滾動捲軸的動作，使瀏覽器讀取更多圖片



```
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
        if str(type(image.get_attribute('src'))) != "<class 'NoneType'>":
            if 'ytimg' in image.get_attribute('src') or '720.jpg?' in image.get_attribute('src') or 'hqdefault.jpg?' in image.get_attribute('src'):
                if len(yt_vedio_images)<10:
                    yt_vedio_images.append(image.get_attribute('src'))
                    print(image.get_attribute('src'))

```



6.獲得影片標題、影片發布者頻道圖片與頻道名稱


```
    #建立標題列表
    yt_title_list = []
    yt_vedio_infos = driver.find_elements_by_css_selector('#video-title')
    for infos in yt_vedio_infos:
        yt_title_list.append(infos.get_attribute('title'))
        print(infos.get_attribute('title'))

    #建立頻道資訊列表(圖片)
    yt_channel_infos_image_urls = []
    yt_channel_infos_image_list = driver.find_elements_by_css_selector('#channel-info a yt-img-shadow #img')
    for infos in yt_channel_infos_image_list:
        yt_channel_infos_image_urls.append(infos.get_attribute('src'))
        print(infos.get_attribute('src'))

    #建立頻道資訊列表(頻道名稱)
    yt_channel_infos_names = []
    yt_channel_infos_name_list = driver.find_elements_by_css_selector('#channel-info ytd-channel-name div#container div#text-container yt-formatted-string a')
    for infos in yt_channel_infos_name_list:
        yt_channel_infos_names.append(infos.text)

    #關閉瀏覽器連線
    driver.close()
```



7.將爬取到的網頁內容以FlexMessage的訊息格式return至app.py



```
    message = []   
   
    #瀏覽器螢幕截圖
    #建立一個隨機4碼的字串，使圖片縮圖瀏覽不會因為讀取同一個url快取而重覆
    random_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
    #message.append(ImageSendMessage(original_content_url=HEROKU_APP_URL + '/static/tmp/test.png?'+random_code,preview_image_url=HEROKU_APP_URL + '/static/tmp/test.png?'+random_code))

    #回傳搜尋結果的FlexMessage
    message.append(image_carousel('YT搜尋結果',yt_vedio_images,vedio_url_list,yt_title_list,yt_channel_infos_image_urls,yt_channel_infos_names))
    return message
```



# flex_msg.py   將圖片/文字/連結組合

1.到(flex simulator)[https://developers.line.biz/flex-simulator/]設計適合的圖文組合

2.將bubble單元之JSON檔案複製至flex_msg.py當中，並將圖片/文字與連結置入，以完成設定



```
def image_carousel(alt_text,image_url_list,vedio_url_list,title_list,yt_channel_infos_image_urls,yt_channel_infos_names):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for image_url, vedio_url, title, channel_img, channel_name in zip(image_url_list,vedio_url_list,title_list,yt_channel_infos_image_urls,yt_channel_infos_names):
        if i<10:
            bubble =    {   "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": image_url + '?',
                                "size": "full",
                                "aspectRatio": "16:9",
                                "aspectMode": "cover",
                                "action": {
                                "type": "uri",
                                "uri": vedio_url
                                }
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": title[:30] if len(title)<30 else title[:30] + '...',
                                    "size": "sm",
                                    "wrap": True,
                                    "contents": []
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "image",
                                        "url": channel_img + '?',
                                        "animated": True,
                                        "size": "xxs",
                                        "align": "start",
                                        "flex": 0,
                                        "aspectMode": "cover"
                                    },
                                    {
                                        "type": "text",
                                        "text": channel_name,
                                        "size": "xs",
                                        "align": "start",
                                        "gravity": "center",
                                        "margin": "md"
                                    }
                                    ],
                                    "margin": "md"
                                }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "action": {
                                    "type": "uri",
                                    "label": "分享",
                                    "uri": 'https://line.me/R/msg/text/?' + vedio_url,
                                    }
                                }
                                ],
                                "flex": 0
                            }
                            }
            contents['contents'].append(bubble)
            i+=1
    print(contents)
    message = FlexSendMessage(alt_text=alt_text,contents=contents)
    return message
```



3.將FlexMessage回傳至app.py回覆給使用者

# LINEBOT範例指令

1.YT,關鍵字：以半形逗號分隔，後面輸入想要在youtube上面搜尋的關鍵字，送出後等待爬蟲獲取資料，將回傳最多10則的Carousel訊息。

<br><br>
====================================<br>
如果喜歡這個教學內容<br>
歡迎訂閱Youtube頻道<br>
[Maso的萬事屋](https://www.youtube.com/playlist?list=PLG4d6NSc7_l5-GjYiCdYa7H5Wsz0oQA7U)<br>
或加LINE私下交流 LINE ID: mastermaso<br>
![LOGO](https://yt3.ggpht.com/ytc/AKedOLR7I7tw_IxwJRgso1sT4paNu2s6_4hMw2goyDdrYQ=s88-c-k-c0x00ffffff-no-rj)<br>


====================================<br>
