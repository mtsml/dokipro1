import json
import os
import time
from bs4 import BeautifulSoup
import requests
import dynamo
import linebot


# めざまし占い
URL_MEZAMASHI_URANAI = 'http://fcs2.sp2.fujitv.co.jp/fortune.php'

# メッセージ
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'

# 設定時間
CONFIG_LONG_TIME_NO_SEE = 200000


def main():
    items = dynamo.get_user_info_all()

    for item in items:
        msg = fortune_today(item['seiza'])
        print('FORTUNE!')
        print('name: ', item['display_name'])
        print('message: ', msg)
        linebot.send_message(item['user_id'], msg)
  
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
            linebot.send_message(item['user_id'], MESSAGE_LONG_TIME_NO_SEE)
            print('message: ', MESSAGE_LONG_TIME_NO_SEE)


if __name__ == '__main__':
    main()
