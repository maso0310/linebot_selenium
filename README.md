# LINEBOT / Selenium / FlexMessaage

操作步驟：

1.下載範例程式碼，切換到範例檔案資料夾

```
git clone https://github.com/maso0310/linebot_selenium.git
cd linebot_selenium
```

2.在heroku設定chromedirver安裝環境，進入APP頁面後，從Settings中點選Add bulidpack，新增以下URL，在Heroku環境中安裝Google Chrome與ChromeDriver。設定完畢後將在下次程式部署Heroku時安裝，會使部署時間與變長，占用容量也會提高。

```
https://github.com/heroku/heroku-buildpack-google-chrome
https://github.com/heroku/heroku-buildpack-chromedriver
```

![heroku settings](https://i.imgur.com/BXypZx0.jpg)

![heroku bulidpacks](https://i.imgur.com/SLgbH6K.jpg)

3.範例程式碼中更改Channel AccessToken與Channel Secret

4.將範例程式碼部署至Heroku App

5.LINEBOT試運行

### IG_image_parser.py





====================================
如果喜歡這個教學內容
歡迎訂閱Youtube頻道
[Maso的萬事屋](https://www.youtube.com/playlist?list=PLG4d6NSc7_l5-GjYiCdYa7H5Wsz0oQA7U)
或加LINE私下交流 LINE ID: mastermaso

====================================
