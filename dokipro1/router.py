import random
from flask import Blueprint, request, abort, render_template
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent, 
    MessageEvent, 
    TextMessage, 
    UnfollowEvent
)    
import a3rt
import dynamo
import const
import util


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
    print('user_id: ', user_id)
    print('message: ', event.message.text)

    key = {
        'user_id': user_id
    }
    point = const.LOVE_POINT_OF_MESSAGE + random.randrange(10)
    dynamo.upd_user_info(key, point, timestamp)

    # COVID19対応
    if event.message.text == const.COVID19:
        message = util.get_covid19_info(const.TODAY)
    else:
        message = a3rt.get_reply_message(event.message.text)

    util.reply(event.reply_token, message)


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