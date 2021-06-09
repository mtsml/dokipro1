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
   
import dokipro1.a3rt as a3rt
import dokipro1.const as const
import dokipro1.dynamo as dynamo
import dokipro1.util as util
import dokipro1.keiba as keiba


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
    elif text == const.CAT: message = util.get_cat_image()
    elif text == const.KEIBA:
        message = keiba.get_race_choice_message()
        util.reply_flex_message(event.reply_token, 'FlexMenu', message)
        return
    else:                     message = a3rt.get_reply_message(text)

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