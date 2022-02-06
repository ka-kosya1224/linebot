from cgitb import handler
from crypt import methods
from os import abort
from flask import Flask, request
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage


app = Flask(__name__)

linebot_api = LineBotApi("L5NygiSYtBXYDI13ALixITajWjukHApCj7Y9o7KO1faJeulgCBnovq/5ez0wLaT6bPD6qQ1UhFa2KjoDbDwIaq8PbrdS9ZnqONvmGmMagdOUa/68rioPwS/J99Pq+PW4xzU2+gTMr5jua7/OxIMJmgdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("3efc330ae09bcaa4f45c99cdda23e258")

#URLを指定すればWebhookからイベントが送られてくるようになった
@app.route("/callback",methods=['POST'])
def callback():
    #リクエストがline platfromから送られてきたか確認するためにサインを認証する必要がある
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#WebhookHandlerに送られてきたイベントを処理する関数を追加する
@handler.add(MessageEvent,message=TextMessage)#１つ目の引数:イベントの種類、２つ目の引数:メッセージの種類
def handle_message(event):
    #LINEから送られてきたメッセージが格納される
    message = event.message.text
    if message=='atcoder':
        reply = 'https://atcoder.jp/users/kosakana1224'
    elif message=='twitter':
        reply = 'https://twitter.com/Sub_kosacr'
    else:
        reply = '勉強しろ'
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=reply))


if __name__=='__main__':
    app.run()
