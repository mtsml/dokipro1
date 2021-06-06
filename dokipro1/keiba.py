import random
import json
import re
import os
import requests
from bs4 import BeautifulSoup


RACE_INFO_URL = 'https://race.netkeiba.com/race/shutuba.html?race_id={}&rf=special_sidemenu'


def get_race_choice_message():
    dirname = os.getcwd()
    path = os.path.join(dirname, 'dokipro1/assets/keiba_choice.json')
    data = open(path, mode='r')
    message = json.load(data)
    data.close()
    return message


def guess_horse_racing(race_id):
    """
    競馬を当てる。

    Parameters
    ----------
    race_id : int
        netkeibaのrace_id。疑似乱数のseedとしても利用する。

    Returns
    -------
    message : str
        3着までの馬番。
        例：「10 18 11」
    """

    res = requests.get(RACE_INFO_URL.format(race_id))
    res.encoding = 'EUC-JP'
    soup = BeautifulSoup(res.text, 'html.parser')
    race_name = get_race_name_from_soup(soup)
    horse_list = get_horse_list_from_soup(soup)
    print(race_name)
    print(horse_list)

    # 同一レースに対して常に同じ結果を返却するためにseedを設定する
    random.seed(race_id)
    # horse_listは頭数+1であるためrangeの最大値にサイズをそのまま指定する
    sanrentan = random.sample(range(1, len(horse_list)), 3)
    message = build_sanrentan_message(race_name, horse_list, sanrentan)

    return message


def get_race_name_from_soup(soup):
    """
    出馬表のsoupからレース情報を返却する。
    """
    race_name = soup.find('div', class_='RaceName').get_text()
    return race_name


def get_horse_list_from_soup(soup):
    """
    出馬表のsoupから出走する馬のリストを返却する。
    """
    tr_all = soup.find_all('tr', class_='HorseList')

    # インデックスと馬番を対応させるために1つサイズの大きいリストを作成する
    horse_list = [None] * (len(tr_all) + 1)
    for tr in tr_all:
        umaban = tr.find('td', class_=re.compile('^Umaban.+')).get_text()
        horse_info = {
            'umaban': umaban,
            'horse_name': tr.find('span', class_='HorseName').a.get_text(),
            'jockey': tr.find('td', class_='Jockey').a.get_text()
        }
        horse_list[int(umaban)] = horse_info

    return horse_list


def build_sanrentan_message(race_name, horse_list, sanrentan):
    """
    三連単のFlexMessageを作成し返却する
    """

    # templateを読み込む
    dirname = os.getcwd()
    path = os.path.join(dirname, 'dokipro1/assets/sanrentan.json')
    data = open(path, mode='r')
    template = json.load(data)
    data.close()

    # レース情報を書き込む
    template['body']['contents'][0]['text'] = race_name

    # 馬の情報を書き込む
    for index, umaban in enumerate(sanrentan):
        horse_info = horse_list[umaban]
        template['body']['contents'][2]['contents'][index*2]['contents'][0]['text'] = horse_info['umaban']
        template['body']['contents'][2]['contents'][index*2]['contents'][1]['contents'][0]['text'] = horse_info['horse_name']
        template['body']['contents'][2]['contents'][index*2]['contents'][1]['contents'][1]['text'] = horse_info['jockey']

    return template