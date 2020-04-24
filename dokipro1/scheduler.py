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
URL_COVID19_TOKYO = 'https://stopcovid19.metro.tokyo.lg.jp/'

# メッセージ
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'


# 設定時間
CONFIG_LONG_TIME_NO_SEE = 200000


def main():
    items = dynamo.get_user_info_all()

    for item in items:
        fortune_today(item)
        tech_news(item)
        covid19_info(item)
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

    message = '本日のテクノロジーニュースです\n\n'
    message += get_teck_news_message(soup, 1) + '\n\n'
    message += get_teck_news_message(soup, 2) + '\n\n'
    message += get_teck_news_message(soup, 3)

    print('TECH NEWS!')
    print('name', item['display_name'])
    send_message(item['user_id'], message)


def get_teck_news_message(soup, index):
    a = soup.find_all('h3', class_='entrylist-contents-title')[index].a
    url = a.get('href')
    title = a.get_text()
    return title + '\n' + url


def covid19_info(item):
    res = requests.get(URL_COVID19_TOKYO)
    soup = BeautifulSoup(res.text, 'html.parser')

    message = '昨日の東京都のコロナ陽性患者数は'
    message += soup.find(class_='DataView-DataInfo-summary').get_text(',').split(',')[0].strip()
    message += '人でした。\n'
    message += soup.find(class_='DataView-DataInfo-date').get_text()

    print('COVID19')
    print('name', item['display_name'])
    send_message(item['user_id'], message)


def send_message(user_id, text):
    line_bot_api.push_message(
        user_id, TextSendMessage(text=text))


if __name__ == '__main__':
    # main()
    print(covid19_info(None))