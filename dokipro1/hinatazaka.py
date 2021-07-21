import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import dokipro1.util as util


HINATAZAKA_HOST = 'https://www.hinatazaka46.com'
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
        article_url = HINATAZAKA_HOST + article.find('a', class_='c-button-blog-detail').get('href')

        bubble_json["hero"]["url"] = image_url
        bubble_json["body"]["contents"][0]["text"] = article.find('div', class_='c-blog-article__title').string.strip()
        bubble_json["body"]["contents"][1]["contents"][0]["text"] = article.find('div', class_='c-blog-article__name').string.strip()
        bubble_json["body"]["contents"][2]["contents"][0]["text"] = to_short_text(article.find('div', class_='c-blog-article__text'))
        bubble_json["body"]["contents"][3]["contents"][0]["action"]["uri"] = article_url
        bubble_json["footer"]["contents"][0]["action"]["data"] = f'hinatazaka,{article_url}'

        json["contents"].append(bubble_json)

    return json


def to_short_text(article):
    # ブログ内でSEPARATERの文字列が使われていたらおしまい
    SEPARATER = ','
    return ' '.join([x.strip() for x in article.get_text(SEPARATER).split(SEPARATER) if x.strip() != ''])[:49] + '…'


def get_image_url_list(article_url):
    res = requests.get(article_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    article = soup.find('div', class_='p-blog-article')
    image_list = article.find_all('img')
    image_url_list = [image.get('src') for image in image_list]
    return image_url_list
