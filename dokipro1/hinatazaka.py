import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import dokipro1.util as util

HINATAZAKA_URL = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&dy={}'


def get_article_list():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    res = requests.get(HINATAZAKA_URL.format(yesterday))
    soup = BeautifulSoup(res.text, 'html.parser')
    article_list = soup.find_all('div', class_='p-blog-article')

    return article_list

def build_hinatazaka_json():
    base_path = 'dokipro1/assets/hinatazaka_base.json'
    bubble_path = 'dokipro1/assets/hinatazaka_bubble.json'
    json = util.get_json(base_path)
    for article in get_article_list():
        bubble_json = util.get_json(bubble_path)
        image_url = article.find('img').get('src')

        bubble_json["hero"]["url"] = image_url
        bubble_json["body"]["contents"][0]["text"] = article.find('div', class_='c-blog-article__title').string.strip()
        bubble_json["body"]["contents"][1]["contents"][0]["text"] = article.find('div', class_='c-blog-article__name').string.strip()
        bubble_json["footer"]["contents"][0]["action"]["uri"] = image_url

        json["contents"].append(bubble_json)

    return json
