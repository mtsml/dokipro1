import random

from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage, ImageSendMessage
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


def reply_flex_message(reply_token, alt_text, contents):
    line_bot_api.reply_message(
        reply_token = reply_token,
        messages = FlexSendMessage(
            alt_text=alt_text,
            contents=contents
        )
    )


def reply_image_message(reply_token, image_message):
    line_bot_api.reply_message(
        reply_token = reply_token,
        messages = image_message
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


def get_cat_image():
    res = requests.get(const.URL_CAT_API)
    json_data = res.json()
    url = json_data['webpurl']
    image_message = ImageSendMessage(
        original_content_url=url,
        preview_image_url=url
    )
    return image_message
