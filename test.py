from urllib.parse import quote  
str = '【Maso的萬事屋】LINE聊天機器人十大常見問題｜1小時精選問答｜程式設計｜Python'
text = str.encode('utf8')

print(text)

text = quote(str.encode('utf8'))
print(text)