from flask import Flask, request, abort, render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage
)

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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

@app.route("/index")
def index():
    push_message('U83ec507bb50826ce2df5a4fa13b112d3')
    return 'Hello World!'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    print('name: ' + display_name)
    print('user_id: ' + user_id)
    print('message: ' + event.message.text)

    text='Your name is ' + get_display_name(user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

@handler.add(FollowEvent)
def on_follow(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    picture_url = profiles.picture_url
    status_message = profiles.status_message

    items = {
        'user_id': user_id,
        'display_name': display_name
    }

    # ユーザー情報をDBに保存
    set_user_info(items)

    # メッセージの送信
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text='登録ありがとう')
    )

def push_message(user_id):
    line_bot_api.push_message(
        to=user_id,
        messages=TextSendMessage(text='プッシュ送信'))

def get_display_name(user_id):
    session = boto3.session.Session(
        region_name='ap-northeast-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')
    items = table.get_item(
            Key={
                 "user_id": user_id
            }
        )
    return items['Item']['display_name']

def set_user_info(items):
    session = boto3.session.Session(
        region_name='ap-northeast-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')

    response = table.put_item(
            Item=items
        )

    if response['ResponseMetadata']['HTTPStatusCode'] is not 200:
        # 失敗処理
        print('Error :', response)
    else:
        # 成功処理
        print('Successed :', items['user_id'])
    
    return

if __name__ == "__main__":
    # app.run()
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)