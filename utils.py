import os
from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def push_message(event,message):
    line_bot_api = LineBotApi(channel_access_token)
    if(event.source.type=='group'):
        id=event.source.group_id
    if(event.source.type=='user'):
        id=event.source.user_id
    line_bot_api.push_message(id,TextSendMessage(text=message))

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def display_name(event):
    line_bot_api = LineBotApi(channel_access_token)
    profile = line_bot_api.get_profile(event.source.user_id)
    return profile.display_name

def send_menu(reply_token):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://storage.googleapis.com/petsmao-images/images/2017/10/c16531eda44144f6.jpg',
            title='Menu',
            text='Please select',
            actions=[
                MessageTemplateAction(
                    label='終極密碼',
                    text='game1'
                ),
                MessageTemplateAction(
                    label='猜歌',
                    text='game2'
                ),
                MessageTemplateAction(
                    label='增加歌單',
                    text='addsong'
                ),
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token,message)
    return "OK"


def send_image(reply_token):
    message = ImageSendMessage(
    original_content_url='https://assets.coingecko.com/coins/images/8914/large/boomfav.png?1562799810',
    preview_image_url='https://assets.coingecko.com/coins/images/8914/large/boomfav.png?1562799810'
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"

def send_audio(reply_token,url):
    message = AudioSendMessage(
    original_content_url=url,
    duration=60000  #60s
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return "OK"