import json
import os
import time
import sys
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
import dynamo
import const
import util


def main():
    funcs = sys.argv
    del funcs[0]
    items = dynamo.get_user_info_all()
    datas = {}

    for func in funcs:
        init(func, datas)

    for item in items:
        for func in funcs:
            execute(func, datas[func], item)


def fortune_today(mode, data, item):
    if mode == const.MODE_INIT:
        return get_fortune_data()
    elif mode == const.MODE_EXEC:
        return get_fortune_message(data, item)


def get_fortune_data():
    soup = util.get_soup_by_url(const.URL_MEZAMASHI_URANAI)
    fortune_data = soup.find_all('div', class_='rankArea')
    return fortune_data


def get_fortune_message(data, item):
    seiza = item['seiza']
    info = get_rank_info(data, seiza)
    rank = info.a.div.find_all('span')[0].get_text()
    message = const.MESSAGE_FORTUNE.format(seiza, rank)

    for t in info.section.div.p.get_text(',').split(','):
        message += t + '\n'

    message += '\n'

    for t in info.section.div.table.get_text(',').split(','):
        if t == '\n' : continue
        message += t + '\n'

    return message


def get_rank_info(rank_list, seiza):
    for rank in rank_list:
        if seiza in rank.a.div.get_text():
            return rank


def tech_news(mode, data, item):
    if mode == const.MODE_INIT:
        return util.get_tech_news(3)
    elif mode == const.MODE_EXEC:
        return data


def covid19_info(mode, data, item):
    if mode == const.MODE_INIT:
        return util.get_covid19_info(const.YESTERDAY)
    elif mode == const.MODE_EXEC:
        return data


def remember_me(mode, data, item):
    if mode == const.MODE_INIT:
        return None
    elif mode == const.MODE_EXEC:
        message = None
        ut = time.time()
        diff = int(ut)-int(item['last_datetime']/1000)

        if diff > const.CONFIG_LONG_TIME_NO_SEE:
            message = const.MESSAGE_LONG_TIME_NO_SEE
        
        return message


def init(func, datas):
    data = eval(func)(const.MODE_INIT, None, None)
    datas[func] = data


def execute(func, data, item):
    message = eval(func)(const.MODE_EXEC, data, item)

    if message != None:
        print(func)
        print('name', item['display_name'])
        util.send_message(item['user_id'], message)


if __name__ == '__main__':
    main()