import json
import os
import time
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
import dynamo


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) 


# URL
URL_MEZAMASHI_URANAI = 'http://fcs2.sp2.fujitv.co.jp/fortune.php'
URL_HATENA_TECH_NEWS = 'https://b.hatena.ne.jp/hotentry/it'


# メッセージ
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'


# 設定時間
CONFIG_LONG_TIME_NO_SEE = 200000


def main():
    items = dynamo.get_user_info_all()

    for item in items:
        fortune_today(item)
        tech_news(item)
        remember_me(item)


def fortune_today(item):
    res = requests.get(URL_MEZAMASHI_URANAI)
    soup = BeautifulSoup(res.text, 'html.parser')
    rank_list = soup.find_all('div', class_='rankArea')
    seiza = item['seiza']

    info = get_rank_info(rank_list, seiza)
    rank = info.a.div.find_all('span')[0].get_text()

    text_fortune = 'おはようございます。\n'
    text_fortune += seiza + 'の今日の運勢は' + rank + 'です。\n\n'

    for t in info.section.div.p.get_text(',').split(','):
        text_fortune += t + '\n'

    # 見やすくするため一行開ける
    text_fortune += '\n'

    for t in info.section.div.table.get_text(',').split(','):
        if t == '\n' : continue
        text_fortune += t + '\n'
    
    print('FORTUNE!')
    print('name: ', item['display_name'])
    send_message(item['user_id'], text_fortune)
    

def get_rank_info(rank_list, seiza):
    for rank in rank_list:
        if seiza in rank.a.div.get_text():
            return rank


def remember_me(item):
    ut = time.time()

    diff = int(ut)-int(item['last_datetime']/1000)
    if diff > CONFIG_LONG_TIME_NO_SEE:
        print('LONG TIME NO SEE!')
        print('name: ', item['display_name'])
        send_message(item['user_id'], MESSAGE_LONG_TIME_NO_SEE)


def tech_news(item):
    res = requests.get(URL_HATENA_TECH_NEWS)
    soup = BeautifulSoup(res.text, 'html.parser')
    url = soup.find('h3', class_='entrylist-contents-title').a.get('href')

    message = '本日のテクノロジーニュースです\n\n' + url

    print('TECH NEWS!')
    print('name', item['display_name'])
    send_message(item['user_id'], message)


def send_message(user_id, text):
    line_bot_api.push_message(
        user_id, TextSendMessage(text=text))


if __name__ == '__main__':
    main()