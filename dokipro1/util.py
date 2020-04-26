import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
from bs4 import BeautifulSoup
import a3rt
import dynamo
import const


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


def get_soup_by_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def get_covid19_info(day):
    soup = get_soup_by_url(const.URL_COVID19_TOKYO)

    today = soup.find(class_='DataView-DataInfo-summary').get_text(',').split(',')[0].strip()
    yesterday = soup.find(class_='DataView-DataInfo-date').get_text()
    message = const.MESSAGE_COVID19.format(day, today, yesterday)

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