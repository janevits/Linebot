from flask import Flask, request, abort

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

line_bot_api = LineBotApi('qq/ozyT0HfNnOLOeAnwsair7tmZlxNDVUouHfHKOQfnDafXECVjt/kl1Og0rE1ihya9de9Nn6DLx7vT0Z8NSZll2eefni5CsBz5SoVwFSFEW+sj451nKx6/iyHhwSO5HTWGCjMvQXtIqNMjnLMeHIAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()