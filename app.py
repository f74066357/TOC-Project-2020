import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot import LineBotApi
from fsm import TocMachine
from utils import send_text_message
from utils import send_menu
from utils import send_image
from utils import send_audio
load_dotenv()

machine = TocMachine(
    states=["user", "menu", "game1","guess","hit","game2","song","right","wrong","again","addsong","addname","addurl"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "game1",
            "conditions": "is_going_to_game1",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "game2",
            "conditions": "is_going_to_game2",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "addsong",
            "conditions": "is_going_to_addsong",
        },
        {
            "trigger": "advance",
            "source": "game1",
            "dest": "guess",
            "conditions": "is_going_to_guess",
        },
        {
            "trigger": "advance",
            "source": "guess",
            "dest": "guess",
            "conditions": "guess_again",
        },
        {
            "trigger": "advance",
            "source": "guess",
            "dest": "hit",
            "conditions": "is_going_to_hit",
        },
        {
            "trigger": "advance",
            "source": "game2",
            "dest": "song",
            "conditions": "is_going_to_song",
        },
        {
            "trigger": "advance",
            "source": "song",
            "dest": "wrong",
            "conditions": "is_going_to_wrong",
        },
        {
            "trigger": "advance",
            "source": "song",
            "dest": "again",
            "conditions": "is_going_to_songagain",
        },
        {
            "trigger": "advance",
            "source": "again",
            "dest": "again",
            "conditions": "is_going_to_songagain",
        },
        {
            "trigger": "advance",
            "source": "again",
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": "again",
            "dest": "wrong",
            "conditions": "is_going_to_wrong",
        },
        {
            "trigger": "advance",
            "source": "song",
            "dest": "right",
            "conditions": "is_going_to_right",
        },
        {
            "trigger": "advance",
            "source": "addsong",
            "dest": "addname",
            "conditions": "is_going_to_addname",
        },
        {
            "trigger": "advance",
            "source": "addname",
            "dest": "addurl",
            "conditions": "is_going_to_addurl",
        },
        {
            "trigger": "go_back", 
            "source": ["hit","right","wrong","addurl"],
            "dest": "user"
        },
        
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue   
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )
    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "不要亂~")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
