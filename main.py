import json
from linebot import (LineBotApi, WebhookParser)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, StickerSendMessage)
from system import Configurator
from requester import Requester
from db import FirestoreClient
from line import LineResponse
from ocr_utils import OCRUtils
import uuid


configurator = Configurator("private/config.json")
db = FirestoreClient(configurator)
service_requester = Requester(configurator)
line_response = LineResponse(configurator)
line_bot_api = LineBotApi(configurator.get('line.access_token'))
parser = WebhookParser(configurator.get('line.channel_secret'))


def handle_message(request):
    body = request.get_data(as_text=True)
    print("Request: " + body)
    signature = request.headers['X-Line-Signature']
    events = parser.parse(body, signature)
    for event in events:
        user_id = event.source.user_id
        reply_token = event.reply_token
        
        if event.type == "message":

            if event.message.type == "text":
                message_text = event.message.text
                
                if message_text.lower().startswith(('https://connect.garmin.com/modern/activity/')):
                    #extract running stat from Garmin
                    pass
                elif message_text.lower().startswith(('https://strava.app.link/activity/')):
                    #extract running stat from Strava
                    pass
                else:
                    service_requester.post_dialogflow(request)
                    
            if event.message.type == "image":
                message_id = event.message.id
                ocr_utils = OCRUtils(configurator)
                response, distance, pace, time = ocr_utils.line_ocr_and_translate(message_id, user_id) 
                db.save_user_running(user_id, distance, pace, time)
                line_response.push(data=response)

            if event.message.type == "sticker":
                package_id = 11539
                sticker_id = 52114112
                line_bot_api.reply_message(reply_token, StickerSendMessage(package_id,sticker_id))

        if event.type == "postback": pass

