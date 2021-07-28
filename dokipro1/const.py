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

# メンバーリスト
HINATAZAKA_MEMBER = [
    {"id" : "2", "member_name" : "潮紗理菜"},
    {"id" : "4", "member_name" : "影山優佳"},
    {"id" : "5", "member_name" : "加藤史帆"},
    {"id" : "6", "member_name" : "齊藤京子"},
    {"id" : "7", "member_name" : "佐々木久美"},
    {"id" : "8", "member_name" : "佐々木美玲"},
    {"id" : "9", "member_name" : "高瀬愛奈"},
    {"id" : "10", "member_name" : "高本彩花"},
    {"id" : "11", "member_name" : "東村芽依"},
    {"id" : "12", "member_name" : "金村美玖"},
    {"id" : "13", "member_name" : "河田陽菜"},
    {"id" : "14", "member_name" : "小坂菜緒"},
    {"id" : "15", "member_name" : "富田鈴花"},
    {"id" : "16", "member_name" : "丹生明里"},
    {"id" : "17", "member_name" : "濱岸ひより"},
    {"id" : "18", "member_name" : "松田好花"},
    {"id" : "19", "member_name" : "宮田愛萌"},
    {"id" : "20", "member_name" : "渡邉美穂"},
    {"id" : "21", "member_name" : "上村ひなの"},
    {"id" : "22", "member_name" : "髙橋未来虹"},
    {"id" : "23", "member_name" : "森本茉莉"},
    {"id" : "24", "member_name" : "山口陽世"},
    {"id" : "000", "member_name" : "ポカ"}
]

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
    class HINATAZAKA:
        ID = 'hinatazaka'
