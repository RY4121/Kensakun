from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction  # こ↑こ↓が追加分
)
import os
import wget
app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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
    # wget.getStoreInfo(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='うんこ漏れそう'))
    # text=event.message.text)

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id))


if __name__ == "__main__":
    #    app.run()
    # 追加しましたby Ryoga 2020/3/5
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
