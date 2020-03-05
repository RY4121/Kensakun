from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction, StickerMessage, StickerSendMessage, ImageMessage  # こ↑こ↓が追加分
)
import os
# from io import BytesIO
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


# スタンプが送られてきた時の処理
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id))
    except Exception as e:
        print("error:", e)
        reply_message(
            event, TextSendMessage(text=str(e))
        )


# メッセージが送られてきたときの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # wget.getStoreInfo(event.message.text)
    try:
        # メッセージリストのサンプル
        # messages = [
        #     TextSendMessage(text='うんこ漏れそう'),
        #     TextSendMessage(text=event.message.text)
        # ]

        # LineBotApiのメソッドを用いたときのサンプル
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text='うんこ漏れそう'))

        messages = [TextSendMessage(text='少々お待ちください')]
        # result_listは2重配列
        result_list = wget.getStoreInfo()
        for list in result_list:
            out_text = list[0] + list[1]
            messages.append(TextSendMessage(text=out_text))

        reply_message(event, messages)
    except Exception as e:
        print("error:", e)
        reply_message(
            event, TextSendMessage(text=str(e))
        )


# 画像が送られきた時の処理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # print("handle_image:", event)
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    # image=BytesIO(message_content.content)

    try:
        # result=search_product(image)
        messages = [
            TextSendMessage(text='画像が送信されました')
            # TextSendMessage(text='食品パッケージ/書籍/CD/DVD/ゲームソフト/PCソフトを検索できるよ！')
        ]

        reply_message(event, messages)

    except Exception as e:
        print("error:", e)
        reply_message(
            event, TextSendMessage(text=str(e))
        )


# LineBotApiから呼び出さない。自作
def reply_message(event, messages):
    line_bot_api.reply_message(
        event.reply_token,
        messages=messages
    )


if __name__ == "__main__":
    #    app.run()
    # 追加しましたby Ryoga 2020/3/5
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
