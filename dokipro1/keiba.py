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
    horse_list = get_horse_list_from_soup(soup)
    print(horse_list)

    # 同一レースに対して常に同じ結果を返却するためにseedを設定する
    random.seed(race_id)
    # horse_listは頭数+1であるためrangeの最大値にサイズをそのまま指定する
    sanrentan = random.sample(range(1, len(horse_list)), 3)
    message = ' '.join(map(str, sanrentan))

    return message


def get_horse_list_from_soup(soup):
    """
    出馬表のURLから出走する馬のリストを返却する。
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
