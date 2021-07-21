import random
import requests
from bs4 import BeautifulSoup
import dokipro1.util as util

HINATAZAKA_URL = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&dy={}'


def get_article_list(date = '20210720'):
    res = requests.get(HINATAZAKA_URL.format(date))
    soup = BeautifulSoup(res.text, 'html.parser')
    article_list = soup.find_all('div', class_='p-blog-article')

    return article_list

def build_hinatazaka_json():
    base_path = 'dokipro1/assets/hinatazaka_base.json'
    bubble_path = 'dokipro1/assets/hinatazaka_bubble.json'
    json = util.get_json(base_path)
    for article in get_article_list():
        bubble_json = util.get_json(bubble_path)
        bubble_json["hero"]["url"] = article.find('img').get('src')
        bubble_json["body"]["contents"][0]["text"] = article.find('div', class_='c-blog-article__title').string
        bubble_json["body"]["contents"][1]["contents"][0]["text"] = article.find('div', class_='c-blog-article__name').string
        json["contents"].append(bubble_json)

    return json
