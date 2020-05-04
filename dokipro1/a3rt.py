import os

import pya3rt

import dokipro1.const as const


def get_reply_message(text):
    client = pya3rt.TalkClient(const.A3RT_TALK_API_KEY)
    res = client.talk(text)
    print(res)

    # 正常終了以外はデフォルトメッセージを返却する
    if res['status'] != 0:
        return const.MESSAGE_REPLY_DEFAULT
    
    reply = res['results'][0]['reply']

    return reply