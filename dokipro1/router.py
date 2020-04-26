import datetime
import json
import os
import random
import logging
from flask import Blueprint, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent, TemplateSendMessage, MessageAction, ConfirmTemplate, PostbackAction, PostbackEvent
from bs4 import BeautifulSoup
import requests
import a3rt
import dynamo
import const


router = Blueprint('router', __name__)

# LINE Messesaging API
line_bot_api = LineBotApi(const.CHANNEL_ACCESS_TOKEN) 
handler = WebhookHandler(const.CHANNEL_SECRET)


@router.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@router.route("/index.html")
def index():
    items = dynamo.get_user_info_all()
    return render_template("index.html", items=items)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    timestamp = event.timestamp
    print('name: ', display_name)
    print('user_id: ', user_id)
    print('message: ', event.message.text)

    key = {
        'user_id': user_id
    }

    point = const.LOVE_POINT_OF_MESSAGE + random.randrange(10)

    # ユーザー情報更新
    dynamo.upd_user_info(key, point, timestamp)

    # COVID19対応
    if event.message.text == const.COVID19:
        message = covid19_info()
    else:
        # 返答メッセージを取得する
        message = a3rt.get_reply_message(event.message.text)

    # メッセージの送信
    reply(event.reply_token, message)


@handler.add(FollowEvent)
def handle_follow_event(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name

    items = {
        'user_id': user_id,
        'display_name': display_name,
        'love_point': const.LOVE_POINT_DEFAULT,
        'message_count': 0
    }

    # ユーザー情報をDBに保存
    dynamo.set_user_info(items)

    # メッセージの送信
    reply(reply_token, const.MESSAGE_AFTER_FOLLOW)


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id

    key = {
        'user_id': user_id,
    }

    # ユーザー情報をDBから削除
    dynamo.del_user_info(key)


@handler.add(PostbackEvent)
def handle_postback_event(event):
    user_id = event.source.user_id
    data = eval(event.postback.data)

    if data.action=='yes':
        postback_yes_action(user_id, data.name)
    else:
        postbak_no_action(user_id)


def postback_yes_action(user_id, name):
    key = {
        'user_id': user_id
    }
    dynamo.upd_display_name(key, name)

    line_bot_api.push_message(
        user_id,
        const.MESSAGE_POSTBACK_YES
    )


def postbak_no_action(user_id):
    line_bot_api.push_message(
        user_id,
        const.MESSAGE_POSTBACK_NO
    )


def reply(reply_token, text):
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text=text)
    )


def confirm(user_id, alt_text, text, actions):
    text_message = TemplateSendMessage(
        alt_text=alt_text,
        template=ConfirmTemplate(
            text=text,
            actions=actions
        )
    )
    line_bot_api.push_message(user_id, text_message)


def covid19_info():
    res = requests.get(const.URL_COVID19_TOKYO)
    soup = BeautifulSoup(res.text, 'html.parser')

    today = soup.find(class_='DataView-DataInfo-summary').get_text(',').split(',')[0].strip()
    yesterday = soup.find(class_='DataView-DataInfo-date').get_text()
    message = const.MESSAGE_COVID19.format(today, yesterday)

    return message