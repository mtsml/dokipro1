from flask import Flask, request, abort, render_template
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent
import boto3
import json

app = Flask(__name__)

# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# AWS
AWS_REGION = 'ap-northeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# love point
LOVE_POINT_DEFAULT = 0
LOVE_POINT_OF_MESSAGE = 1

# Template Messages
MESSAGE_AFTER_FOLLOW = 'これからよろしくお願いします、{0}先輩。'

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    print('name: ', display_name)
    print('user_id: ', user_id)
    print('message: ', event.message.text)

    # love point増加
    upd_love_point(user_id, LOVE_POINT_OF_MESSAGE)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

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
    set_user_info(items)

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
    del_user_info(key)

def conn_dynamodb():
    session = boto3.session.Session(
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return session

def set_user_info(items):
    session = conn_dynamodb()
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

def del_user_info(key):
    session = conn_dynamodb()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')

    response = table.delete_item(
            Key=key
        )

    if response['ResponseMetadata']['HTTPStatusCode'] is not 200:
        # 失敗処理
        print('Error :', response)
    else:
        # 成功処理
        print('Successed :', key['user_id'])

def upd_love_point(key, point):
    session = conn_dynamodb()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')

    response = table.update_item(
        Key=key,
        UpdateExpression="set love_point = love_point + :val",
        ExpressionAttributeValues={
            ':val': point
        }
    )

if __name__ == "__main__":
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)