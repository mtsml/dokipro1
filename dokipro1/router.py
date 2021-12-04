# -*- coding: utf-8 -*-
import os
import random

from flask import Blueprint, request, abort, render_template
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent,
    MessageEvent,
    TextMessage,
    UnfollowEvent,
    PostbackEvent
)

from a3rt import A3rt
import dokipro1.const as const
import dokipro1.dynamo as dynamo
import dokipro1.util as util
import dokipro1.keiba as keiba
import dokipro1.hinatazaka as hinatazaka


# A3RT
A3RT_TALK_API_KEY = os.environ['A3RT_TALK_API_KEY']


router = Blueprint('router', __name__)
handler = WebhookHandler(const.CHANNEL_SECRET)


@router.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return const.OK


@router.route("/index.html")
def index():
    items = dynamo.get_user_info_all()
    return render_template("index.html", items=items)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    timestamp = event.timestamp
    text = event.message.text
    print('user_id: ', user_id)
    print('message: ', event.message.text)

    key = {
        'user_id': user_id
    }
    point = const.LOVE_POINT_OF_MESSAGE + random.randrange(10)
    dynamo.upd_user_info(key, point, timestamp)

    message= None
    if text == const.COVID19: message = util.get_covid19_info(const.TODAY)
    elif text == const.NEWS:  message = util.get_tech_news(3)
    elif text == const.CAT:
        message = util.get_cat_image()
        util.reply_image_message(event.reply_token, message)
        return
    elif text == const.POKEMON:
        message = util.get_pokemon_image()
        # message = keiba.get_pokemon_quiz_message()
        util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        # util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        return
    elif text == const.KEIBA:
        message = keiba.get_race_choice_message()
        util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        return
    elif text == const.HINATAZAKA:
        message = util.get_json('dokipro1/assets/hinatazaka_member.json')
        util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        return
    elif hinatazaka.is_hinatazaka_member(text):
        message = hinatazaka.build_hinatazaka_json(hinatazaka.get_member_list(text))
        util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        return
    else:
        a3rt = A3rt(A3RT_TALK_API_KEY)
        message = a3rt.talk(text)

    util.reply(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_postback_event(event):
    """
    ボタン押下などのアクションを処理する
    """

    user_id = event.source.user_id
    timestamp = event.timestamp
    action_id, data = event.postback.data.split(',')
    print('user_id: ', user_id)
    print('action_id: ', action_id)
    print('data: ', data)

    if action_id == const.ACTION.KEIBA.ID:
        message = keiba.guess_horse_racing(int(data))
        util.reply_flex_message(event.reply_token, 'sanrentan', message)
    elif action_id == const.ACTION.POKEMON.ID:
        message = '残念'
        if data == 'true':
            message = '正解!!'
        util.reply(event.reply_token, message)
    elif action_id == const.ACTION.HINATAZAKA.ID:
        util.reply(event.reply_token, '少々お待ちください。')
        for image_url in hinatazaka.get_image_url_list(data):
            util.send_image(user_id, image_url)


@handler.add(FollowEvent)
def handle_follow_event(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    profiles = util.line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name

    items = {
        'user_id': user_id,
        'display_name': display_name,
        'love_point': const.LOVE_POINT_DEFAULT,
        'message_count': 0
    }
    dynamo.set_user_info(items)

    util.reply(reply_token, const.MESSAGE_AFTER_FOLLOW)


@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    user_id = event.source.user_id

    key = {
        'user_id': user_id,
    }
    dynamo.del_user_info(key)
