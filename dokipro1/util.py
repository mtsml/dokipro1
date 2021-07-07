import random
import json
import os

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


def get_pokemon_image():
    id = str(random.randrange(1, 899, 1))
    res = requests.get('https://pokeapi.co/api/v2/pokemon/' + id + '/')
    json_data = res.json()
    # url = json_data['webpurl']
    image_url =json_data['sprites']['front_default']
    message = build_pokemon_message (image_url)
    # image_message = ImageSendMessage(
    #     original_content_url=image,
    #     preview_image_url=image
    # )
    return message

def build_pokemon_message(pokemon_image):
    """
    三連単のFlexMessageを作成し返却する
    """

    # templateを読み込む
    dirname = os.getcwd()
    path = os.path.join(dirname, 'dokipro1/assets/quiz_base.json')
    data = open(path, mode='r')
    template = json.load(data)
    data.close()

    # ポケモンイメージを書き込む
    template['body']['contents'][0]['contents'][0]['url'] = pokemon_image

    # 馬の情報を書き込む
    # for index, umaban in enumerate(sanrentan):
    #     horse_info = horse_list[umaban]
    #     template['body']['contents'][2]['contents'][index*2]['contents'][0]['text'] = horse_info['umaban']
    #     template['body']['contents'][2]['contents'][index*2]['contents'][1]['contents'][0]['text'] = horse_info['horse_name']
    #     template['body']['contents'][2]['contents'][index*2]['contents'][1]['contents'][1]['text'] = horse_info['jockey']

    return template
