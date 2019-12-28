from flask import Flask, request, abort, render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route("/index")
def index():
    push_message('U83ec507bb50826ce2df5a4fa13b112d3')
    return 'Hello World!'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profiles = line_bot_api.get_profile(user_id=user_id)
    display_name = profiles.display_name
    print('name: ' + display_name)
    print('user_id: ' + user_id)
    print('message: ' + event.message.text)

    if '好き' in event.message.text:
        text='私も好き'
    else:
        text=event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))

def push_message(user_id):
    line_bot_api.push_message(
        to=user_id,
        messages=TextSendMessage(text='プッシュ送信'))

if __name__ == "__main__":
    # app.run()
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)