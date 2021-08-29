from linebot.models import *

def image_carousel(alt_text,image_url_list,vedio_url_list,title_list):
    contents = dict()
    contents['type'] = 'carousel'
    contents['contents'] = []
    i=0
    for image_url, vedio_url, title in zip(image_url_list,vedio_url_list,title_list):
        if i<10:
            bubble =    {
                            "type": "bubble",
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
                                    "text": title,
                                    "size": "sm",
                                    "wrap": True
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
                                    "uri": "https://linecorp.com"
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
