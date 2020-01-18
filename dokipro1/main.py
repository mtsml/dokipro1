import datetime
import json
import os
import random
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent
import a3rt
import dynamo


app = Flask(__name__)


# love point
LOVE_POINT_DEFAULT = 0
LOVE_POINT_OF_MESSAGE = 1


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) 
handler = WebhookHandler(CHANNEL_SECRET)


# Template Messages
MESSAGE_AFTER_FOLLOW = 'これからよろしくお願いします、{0}先輩。'
MESSAGE_REPLY_DEFAULT = '認識できませんでした'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@app.route("/index.html")
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

    point = LOVE_POINT_OF_MESSAGE + random.randrange(10)

    # ユーザー情報更新
    dynamo.upd_user_info(key, point, timestamp)

    # 返答メッセージを取得する
    reply = a3rt.get_reply_message(event.message.text)

    reply_message(event.reply_token, reply)


@handler.add(FollowEvent)
def handle_follow_event(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    text = MESSAGE_AFTER_FOLLOW.format(display_name)

    items = {
        'user_id': user_id,
        'display_name': display_name,
        'love_point': LOVE_POINT_DEFAULT
    }

    # ユーザー情報をDBに保存
    dynamo.set_user_info(items)

    # メッセージの送信
    reply_message(event.reply_token, text)


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id

    key = {
        'user_id': user_id,
    }

    # ユーザー情報をDBから削除
    dynamo.del_user_info(key)


def reply_message(reply_token, text):
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text=text)
    )


if __name__ == "__main__":
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)