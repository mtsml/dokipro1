import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import dokipro1.util as util
import dokipro1.const as const


HINATAZAKA_HOST = 'https://www.hinatazaka46.com'
HINATAZAKA_URL = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&dy={}'
HINATAZAKA_MEMBER_URL = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000&ct={}'
HINATAZAKA_IMAGE_HOST = 'https://cdn.hinatazaka46.com'
HINATAZAKA_OFFICIAL_LOGO = 'https://cdn.hinatazaka46.com/files/14/hinata/img/logo_side.svg'


def get_article_list():
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    soup = util.get_soup_by_url(HINATAZAKA_URL.format(yesterday))
    article_list = soup.find_all('div', class_='p-blog-article')

    return article_list

def get_member_list(name):
    id = ""
    for member in const.HINATAZAKA_MEMBER:
        if member["member_name"] == name:
            id = member["id"]
            break
    soup = util.get_soup_by_url(HINATAZAKA_MEMBER_URL.format(id))
    article_list = soup.find_all('div', class_='p-blog-article').slice[:3]

    return article_list

def build_hinatazaka_json(article_list):
    base_path = 'dokipro1/assets/hinatazaka_base.json'
    bubble_path = 'dokipro1/assets/hinatazaka_bubble.json'
    json = util.get_json(base_path)
    for article in article_list:
        bubble_json = util.get_json(bubble_path)
        image_url_list = get_alive_image_url_list(article)
        image_url = image_url_list[0] if len(image_url_list) > 0 else HINATAZAKA_OFFICIAL_LOGO
        article_url = HINATAZAKA_HOST + article.find('a', class_='c-button-blog-detail').get('href')

        bubble_json["hero"]["url"] = image_url
        bubble_json["body"]["contents"][0]["text"] = article.find('div', class_='c-blog-article__title').string.strip()
        bubble_json["body"]["contents"][1]["contents"][0]["text"] = article.find('div', class_='c-blog-article__name').string.strip()
        bubble_json["body"]["contents"][2]["contents"][0]["text"] = to_short_text(article.find('div', class_='c-blog-article__text'))
        bubble_json["body"]["contents"][3]["contents"][0]["action"]["uri"] = article_url
        bubble_json["footer"]["contents"][0]["action"]["data"] = f'hinatazaka,{article_url}'

        json["contents"].append(bubble_json)

    return json

def is_hinatazaka_member(name):
    for member in const.HINATAZAKA_MEMBER:
        if member["member_name"] == name:
            return True
    return False

def to_short_text(article):
    # ブログ内でSEPARATERの文字列が使われていたらおしまい
    SEPARATER = ','
    return ' '.join([x.strip() for x in article.get_text(SEPARATER).split(SEPARATER) if x.strip() != ''])[:49] + '…'


def get_image_url_list(article_url):
    soup = util.get_soup_by_url(article_url)
    article = soup.find('div', class_='p-blog-article')
    image_url_list = get_alive_image_url_list(article)

    return image_url_list


def is_image_url_alive(image_url):
    return image_url.startswith(HINATAZAKA_IMAGE_HOST)


def get_alive_image_url_list(article):
    image_list = article.find_all('img')
    image_url_list = [image.get('src') for image in image_list]
    alive_image_url_list = [image_url for image_url in image_url_list if is_image_url_alive(image_url)]

    return alive_image_url_list
