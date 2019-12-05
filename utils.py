import os
from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

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