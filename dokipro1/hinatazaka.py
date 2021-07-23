import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import dokipro1.util as util


HINATAZAKA_HOST = 'https://www.hinatazaka46.com'
HINATAZAKA_URL = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&dy={}'
HINATAZAKA_IMAGE_HOST = 'https://cdn.hinatazaka46.com'
HINATAZAKA_OFFICIAL_LOGO = 'https://cdn.hinatazaka46.com/files/14/hinata/img/logo_side.svg'


def get_article_list():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    soup = get_article(HINATAZAKA_URL.format(yesterday))
    article_list = soup.find_all('div', class_='p-blog-article')

    return article_list


def build_hinatazaka_json():
    base_path = 'dokipro1/assets/hinatazaka_base.json'
    bubble_path = 'dokipro1/assets/hinatazaka_bubble.json'
    json = util.get_json(base_path)
    for article in get_article_list():
        bubble_json = util.get_json(bubble_path)
        image_url = article.find('img').get('src')
        image_url = HINATAZAKA_OFFICIAL_LOGO if not is_image_url_alive(image_url)

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
    soup = get_article(article_url)
    article = soup.find('div', class_='p-blog-article')
    image_list = article.find_all('img')
    all_image_url_list = [image.get('src') for image in image_list]
    image_url_list = []
    for image_url in all_image_url_list:
        image_url_list.append(image_url) if is_image_url_alive(image_url)

    return image_url_list


def get_article(article_url):
    res = requests.get(article_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def is_image_url_alive(image_url):
    return image_url.startswith(HINATAZAKA_IMAGE_HOST)
