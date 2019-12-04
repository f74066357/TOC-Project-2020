import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_menu(reply_token, text):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://storage.googleapis.com/petsmao-images/images/2017/10/c16531eda44144f6.jpg',
            title='Menu',
            text='Please select',
            actions=[
                MessageTemplateAction(
                    label='MODE1',
                    text='number'
                ),
                MessageTemplateAction(
                    label='MODE2',
                    text='transportation'
                ),
                URITemplateAction(
                    label='uri',
                    uri='https://moodle.ncku.edu.tw/mod/forum/discuss.php?d=403554'
                )
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(event.reply_token, message)
    return "OK"

"""
def send_image_url(id, img_url):
    message = ImageSendMessage(
    original_content_url='https://example.com/original.jpg',
    preview_image_url='https://example.com/preview.jpg'
    )
    line_bot_api.reply_message(event.reply_token, message)
    return "OK"

def send_button_message(id, text, buttons):
    pass
"""
