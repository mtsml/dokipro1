import os


# LINE Messesaging API
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]


# AWS
AWS_REGION = 'ap-northeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DYNAMO_TABLE_NM = 'dokipro1'


# A3RT
A3RT_TALK_API_KEY = os.environ['A3RT_TALK_API_KEY']


# love point
LOVE_POINT_DEFAULT = 0
LOVE_POINT_OF_MESSAGE = 1


# Messages
MESSAGE_AFTER_FOLLOW = 'フォローありがとうございます。'
MESSAGE_POSTBACK_NO = 'ニックネームを教えて下さい。'
MESSAGE_POSTBACK_YES = '{}さん、これからよろしくお願いします。'
MESSAGE_LONG_TIME_NO_SEE = '私のこと忘れちゃった？'
MESSAGE_COVID19 = '{}の東京都のコロナ陽性患者数は{}人です。\n（前日比: {} 人）'
MESSAGE_TECH_NEWS = '本日のテクノロジーニュースです'
MESSAGE_FORTUNE = 'おはようございます。\n{}の今日の運勢は{}です。\n\n'
MESSAGE_REPLY_DEFAULT = 'ちょっと何言ってるか分からないです'


# 定数
OK = 'OK'
COVID19 = 'コロナ'
TODAY = '本日'
YESTERDAY = '昨日'
MODE_INIT = 1
MODE_EXEC = 2
NEWS = 'ニュース'
CAT = 'にゃーん'
KEIBA = '競馬'
POKEMON = 'ポケモンクイズ'
HINATAZAKA = '日向坂'

# 設定時間
CONFIG_LONG_TIME_NO_SEE = 200000


# URL
URL_COVID19_TOKYO = 'https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/daily_positive_detail.json'
URL_MEZAMASHI_URANAI = 'http://fcs2.sp2.fujitv.co.jp/fortune.php'
URL_HATENA_TECH_NEWS = 'https://b.hatena.ne.jp/hotentry/it'
URL_CAT_API = 'https://thatcopy.pw/catapi/rest/'


# ACTION定義
class ACTION:
    class CAT:
        ID = 'cat'
    class KEIBA:
        ID = 'keiba'
    class POKEMON:
        ID = 'pokemon'
