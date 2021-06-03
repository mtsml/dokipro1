import random

from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
import requests

import dokipro1.const as const


# LINE Messesaging API
line_bot_api = LineBotApi(const.CHANNEL_ACCESS_TOKEN) 


def reply(reply_token, text):
    line_bot_api.reply_message(
        reply_token=reply_token,
        messages=TextSendMessage(text=text)
    )


def send_message(user_id, text):
    line_bot_api.push_message(
        user_id, TextSendMessage(text=text))


def send_flex_message(user_id, alt_text, contents):
    line_bot_api.push_message(
        user_id, FlexSendMessage(
            alt_text=alt_text,
            contents=contents
        )
    )


def get_soup_by_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def get_covid19_data():
    res = requests.get(const.URL_COVID19_TOKYO)
    return res.json()


def get_covid19_info(day):
    data = get_covid19_data()["data"]

    today = int(data[-1]["count"])
    yesterday = int(data[-2]["count"])
    diff = today - yesterday
    if diff >= 0:
        diff = '+' + str(diff)
    message = const.MESSAGE_COVID19.format(day, str(today), str(diff))

    return message


def get_tech_news(count):
    soup = get_soup_by_url(const.URL_HATENA_TECH_NEWS)

    message = const.MESSAGE_TECH_NEWS
    for i in range(count):
        message += '\n\n' + get_tech_news_one(soup, i)

    return message


def get_tech_news_one(soup, index):
    a = soup.find_all('h3', class_='entrylist-contents-title')[index].a
    url = a.get('href')
    title = a.get_text()
    return title + '\n' + url


def guess_horse_racing(seed, horse_cnt):
    """
    競馬を当てる。

    Parameters
    ----------
    seed : int
        疑似乱数に与えるseed。
        形式：「YYYYMMDD」+「場名コード」+「レース番号」
        例：2021年の日本ダービーの場合「202105300511」
    horse_cnt : int
        出走する馬の頭数。

    Returns
    -------
    message : str
        3着までの馬番。
        例：「10 18 11」
    """

    # 同一レースに対して常に同じ結果を返却するためにseedを設定する
    random.seed(seed)
    sanrentan = random.sample(range(1, horse_cnt + 1), 3)
    message = ' '.join(map(str, sanrentan))

    return message