import os

import requests

import dokipro1.const as const

class TalkClient:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.endpoint = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'

    def talk(self, text):
        param = {
            'apikey': self.apiKey,
            'query': text
        }
        print(param)
        res = requests.post(self.endpoint, param)
        return res.json()


def get_reply_message(text):
    client = TalkClient(const.A3RT_TALK_API_KEY)
    res = client.talk(text)
    print(res)

    # 正常終了以外はデフォルトメッセージを返却する
    if res['status'] != 0:
        return const.MESSAGE_REPLY_DEFAULT
    
    reply = res['results'][0]['reply']

    return reply