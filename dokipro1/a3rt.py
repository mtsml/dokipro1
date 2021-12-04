# -*- coding: utf-8 -*-
import requests


MESSAGE_REPLY_DEFAULT = 'ちょっと何言ってるか分からないです'


class A3rt:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.endpoint = 'https://api.a3rt.recruit.co.jp/talk/v1/smalltalk'

    def talk(self, text):
        param = {
            'apikey': self.apiKey,
            'query': text
        }
        print(param)

        response = requests.post(self.endpoint, param)
        response = response.json()
        print(response)

        if response['status'] == 0:
            return response['results'][0]['reply']
        else:
            # 正常終了以外はデフォルトメッセージを返却する
            return MESSAGE_REPLY_DEFAULT
