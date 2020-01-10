import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent
import boto3
import json
import time


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# AWS
AWS_REGION = 'ap-northeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# メッセージ
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'

# 設定時間
CONFIG_LONG_TIME_NO_SEE = 86400


def main():
    items = get_user_info_all()

    ut = time.time()

    for item in items:
        diff = int(ut)-int(item['last_datetime']/1000)
        if diff > CONFIG_LONG_TIME_NO_SEE:
            print('LONG TIME NO SEE!')
            print('name: ', item['display_name'])
            send_message(item['user_id'])
            print('message: ', MESSAGE_LONG_TIME_NO_SEE)


def get_user_info_all():
    session = conn_dynamodb()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')

    response = table.scan()

    if response['ResponseMetadata']['HTTPStatusCode'] is not 200:
        # 失敗処理
        print('Error :', response)
    else:
        # 成功処理
        print('Successed :', response['Items'])
        return response['Items']


def conn_dynamodb():
    session = boto3.session.Session(
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return session


def send_message(user_id):
    line_bot_api.push_message(
        user_id, TextSendMessage(text=MESSAGE_LONG_TIME_NO_SEE))


if __name__ == '__main__':
    main()