import pya3rt
import os


# A3RT
A3RT_TALK_API_KEY = os.environ['A3RT_TALK_API_KEY']


def get_reply_message(text):
    client = pya3rt.TalkClient(A3RT_TALK_API_KEY)
    res = client.talk(text)
    print(res)

    # 正常終了以外はデフォルトメッセージを返却する
    if res['status'] != 0:
        return MESSAGE_REPLY_DEFAULT
    
    reply = res['results'][0]['reply']

    return reply