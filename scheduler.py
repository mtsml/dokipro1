# -*- coding: utf-8 -*-

import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage, TextSendMessage, UnfollowEvent
import boto3
import json
import time
import requests
from bs4 import BeautifulSoup


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# AWS
AWS_REGION = 'ap-northeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# めざまし占い
URL_MEZAMASHI_URANAI = 'http://fcs2.sp2.fujitv.co.jp/fortune.php'

# メッセージ
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'

# 設定時間
CONFIG_LONG_TIME_NO_SEE = 200000


def main():
    items = get_user_info_all()

    for item in items:
        msg = fortune_today(item['seiza'])
        print('FORTUNE!')
        print('name: ', item['display_name'])
        print('message: ', msg)
        send_message(item['user_id'], msg)
  
    # remember_me()

    return


def fortune_today(seiza):
    res = requests.get(URL_MEZAMASHI_URANAI)
    soup = BeautifulSoup(res.text, 'html.parser')
    rank_list = soup.find_all('div', class_='rankArea')

    info = get_rank_info(rank_list, seiza)

    text = 'おはようございます。\n'
    text += seiza + 'の今日の運勢は' + info.a.div.find_all('span')[0].get_text() + 'です。\n\n'

    for t in info.section.div.p.get_text(',').split(','):
        text += t + '\n'

    # 見やすくするため一行開ける
    text += '\n'

    for t in info.section.div.table.get_text(',').split(','):
        if t == '\n' : continue
        text += t + '\n'
    
    return text


def get_rank_info(rank_list, seiza):
    for rank in rank_list:
        if seiza in rank.a.div.get_text():
            return rank


def remember_me():
    items = get_user_info_all()

    ut = time.time()

    for item in items:
        diff = int(ut)-int(item['last_datetime']/1000)
        if diff > CONFIG_LONG_TIME_NO_SEE:
            print('LONG TIME NO SEE!')
            print('name: ', item['display_name'])
            send_message(item['user_id'], MESSAGE_LONG_TIME_NO_SEE)
            print('message: ', MESSAGE_LONG_TIME_NO_SEE)


def get_user_info_all():
    session = conn_dynamodb()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('dokipro1')

    response = table.scan()

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
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


def send_message(user_id, msg):
    line_bot_api.push_message(
        user_id, TextSendMessage(text=msg))


if __name__ == '__main__':
    main()
