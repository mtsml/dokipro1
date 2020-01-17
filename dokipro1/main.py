from flask import Flask, request, abort, render_template
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent
import json
import datetime
import random
import pya3rt
import dynamo

app = Flask(__name__)


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) 
handler = WebhookHandler(CHANNEL_SECRET)


# A3RT
A3RT_TALK_API_KEY = os.environ['A3RT_TALK_API_KEY']


# love point
LOVE_POINT_DEFAULT = 0
LOVE_POINT_OF_MESSAGE = 1


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
    reply = get_reply_message(event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


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
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text=text)
    )


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id

    key = {
        'user_id': user_id,
    }

    # ユーザー情報をDBから削除
    dynamo.del_user_info(key)


def get_reply_message(text):
    client = pya3rt.TalkClient(A3RT_TALK_API_KEY)
    res = client.talk(text)
    print(res)

    # 正常終了以外はデフォルトメッセージを返却する
    if res['status'] != 0:
        return MESSAGE_REPLY_DEFAULT
    
    reply = res['results'][0]['reply']
    print(reply)
    return reply


if __name__ == "__main__":
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)