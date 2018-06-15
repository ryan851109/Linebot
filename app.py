import requests 
from bs4 import BeautifulSoup
import urllib

from linebot.models import *

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ozMuYJFjTwn/fOMSJItnaJ9G8f5/+LyMyjZl0xsIof/BNZSfDa7WGeY8NuENF0Awx8pQTAHkw0wJASsQ4rRE5elMge1NICmJc4q26VBZpIQt19aY2ILJjhy+f94zwaolB1dAxjYJ1CEir1miHAIGaQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('2e4b72dbcdce8f71b04319ed848ab998')

# 監聽所有來自 /callback 的 Post Request
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
	if event.message.text == "最新電影":
		a=movie()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="movie"))
	if event.message.text == "貼圖":
		message = StickerSendMessage(package_id='1',sticker_id='1')
		line_bot_api.reply_message(event.reply_token, message)
	if event.message.text == "youtube":
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text= 'https://www.youtube.com/watch?v=yFz2g7VyfLY' ))
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


	
def movie():
	target_url = 'https://movies.yahoo.com.tw/'
	rs = requests.session()
	res = rs.get(target_url, verify=True)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, 'lxml')   
	content = ""
	print(soup.select('html body div#maincontainer main div.maincontent.ga_index div#container div#content_r div.r_box div.r_box_inner div.ranking_inner_r div.tab-content div#list1 ul.ranking_list_r a'))
	for index , data in enumerate(soup.select('html body div#maincontainer main div.maincontent.ga_index div#container div#content_r div.r_box div.r_box_inner div.ranking_inner_r div.tab-content div#list1 ul.ranking_list_r a')):
		if index == 20:
			return content 
		title = data.text
		link =  data['href']
		content += '{}\n{}\n'.format(title, link)
	return content