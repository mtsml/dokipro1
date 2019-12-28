from flask import Flask, request, abort
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

@app.route("/index", methods=['POST'])
def index():
    return 'Hello World!'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.source.user_id)
    app.logger.info(event.source.user_id)

    if '好き' in event.message.text:
        text='私も好き'
    else:
        text=event.message.text
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))


if __name__ == "__main__":
    # app.run()
    port = int(os.environ["PORT"])
    app.run(host="0.0.0.0", port=port)