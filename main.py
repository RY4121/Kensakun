from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URIAction, StickerMessage, StickerSendMessage, ImageMessage, MessageTemplateAction  # こ↑こ↓が追加分
)
import os
import time
import datetime
# from io import BytesIO
import wget
# import sheetsample as gs
import time_get as tg
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

    messages = []
    push_message(
        event,
        TextSendMessage(text='少々お待ちください')
    )

    if '駅' in event.message.text:
        # call function
        time_info_list = searchBusTime(event.message.text)
        messages = []
        for x in time_info_list:
            messages.append(TextSendMessage(text=x))
        push_message(
            event,
            messages
        )
    else:
        # DMMから検索結果を返す
        # callAvByDmm(event)
        push_message(
            event,
            TextSendMessage(text='大学は楽しいですか？私も行ってみたいです')
        )

    # ButtonsTemplate処理
    message_template = make_button_template()
    push_message(
        event,
        message_template
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


def push_message(event, messages):
    line_bot_api.push_message(
        event.source.user_id,
        messages=messages
    )


def callAvByDmm(event):
    try:
        # reply_message(event, messages)
        # result_listは2重配列
        result_list = wget.getStoreInfo(event.message.text)
        # del result_list[5:]
        if len(result_list) == 0:
            result_list.append(['検索結果', '0'])
            # result_list.append('0')
        for list in result_list:
            out_text1 = list[0]
            out_text2 = list[1]
            # messages.append(TextSendMessage(text=out_text))
            push_message(
                event, [
                    TextSendMessage(text=out_text1),
                    TextSendMessage(text=out_text2)
                ]
            )

        push_message(
            event, [
                TextSendMessage(text='Enjoy masturbation!!')
            ]
        )
    except Exception as e:
        print("error:", e)
        reply_message(
            event, TextSendMessage(text=str(e))
        )


def make_button_template():
    message_template = TemplateSendMessage(
        alt_text="新規メッセージです",
        template=ButtonsTemplate(
            text="大学のバスの時間を教えます",
            title="知りたい情報を以下から選んでください",
            image_size="cover",
            thumbnail_image_url="https://www.shimay.uno/nekoguruma/wp-content/uploads/sites/2/2018/03/20171106_212850.jpg",
            actions=[
                 MessageTemplateAction(
                     label='みなみ野駅発',
                     text='みなみ野駅発'
                 ),
                MessageTemplateAction(
                     label='キャンパス発みなみ野駅行',
                     text='キャンパス発みなみ野駅行'
                 ),
                MessageTemplateAction(
                     label='八王子駅発',
                     text='八王子駅発'
                 ),
                MessageTemplateAction(
                     label='キャンパス発八王子駅行',
                     text='キャンパス発八王子駅行'
                 )

            ]
        )
    )

    return message_template


def searchBusTime(text):
    # time_info = ''
    TYPE = 0
    if datetime.now().strftime('%A') == 'Sunday':
        return '今日のバスの運行はありません'

    if datetime.now().strftime('%A') == 'Saturday':
        OBJECT_URL = 'https://www.teu.ac.jp/campus/access/2020_0307_0314_bus.html'
    else:
        OBJECT_URL = 'https://www.teu.ac.jp/campus/access/2020_0303_0318_bus.html'
    time = tg.Time(OBJECT_URL)

    if text == 'みなみ野駅発':
        TYPE = 1
        tx = time.getData(TYPE)
    elif text == 'キャンパス発みなみ野駅行':
        TYPE = 2
        tx = time.getData(TYPE)
    elif text == '八王子駅発':
        TYPE = 3
        tx = time.getData(TYPE)
    elif text == 'キャンパス発八王子駅行':
        TYPE = 4
        tx = time.getData(TYPE)
    else:
        tx = 'Error'
    time_info = tx
    return time_info


if __name__ == "__main__":
    #    app.run()
    # 追加しましたby Ryoga 2020/3/5
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
