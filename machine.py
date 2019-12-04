import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

machine = TocMachine(
    states=["user", "start1", "start2"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start1",
            "conditions": "is_going_to_start1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start2",
            "conditions": "is_going_to_start2",
        },
        {"trigger": "go_back", "source": ["start1", "start2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
machine.get_graph().draw("fsm.png", prog="dot", format="png")
