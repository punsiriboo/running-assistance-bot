import json
import requests
from system import Configurator
from line import LineResponse


class Requester:

    def __init__(self, config: Configurator):
        self.configurator = config
        self.line = LineResponse(self.configurator)
    
    def post_dialogflow(self, request):
        url = self.configurator.get('dialogflow.webhook')
        headers = dict()
        for key,value in request.headers.items():
            headers[key] = value
        headers['Host'] = self.configurator.get('dialogflow.host')
        r = requests.post(url, data = json.dumps(request.json), headers=headers)
    
    def post_branch_search(self, event):
        user_id = event.source.user_id
        latitude = event.message.latitude
        longitude = event.message.longitude
        url = self.configurator.get('api.location.branch')
        headers = { 'Content-Type': 'application/json'}
        payload = {
            'type': 'postback', 'replyToken': event.reply_token,
            'source': { 'type': 'user', 'userId': user_id },
            'postback': { 'data': 'latitude={}&longitude={}'.format(latitude, longitude) },
            'timestamp': { 'seconds': 0, 'nanos': 0 }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.line.push(data=response.content)


    def post_merchant_search(self, event, merchant_type):
        user_id = event.source.user_id
        latitude = event.message.latitude
        longitude = event.message.longitude
        url = self.configurator.get('api.location.merchant')
        headers = { 'Content-Type': 'application/json'}
        payload = {
            'type': 'postback', 'replyToken': event.reply_token,
            'source': { 'type': 'user', 'userId': user_id },
            'postback': { 'data': 'MerchantType={}&latitude={}&longitude={}'.format(merchant_type, latitude, longitude) },
            'timestamp': { 'seconds': 0, 'nanos': 0 }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.line.push(data=response.content)

        if response.json()['messages'][0]['type'] =='text':
            return False
        else: return True
        

    def post_text_translation(self, user_id, text, target):
        url = self.configurator.get('api.translation.text')
        headers = { 'Content-Type': 'application/json'}
        payload = { 'target': target, 'text': text, 'userId': user_id}
        if target =="check":
            text_mgs = "กำลังตรวจสอบ, กรุณารอสักครู่ 😚"
        else:
            text_mgs = "น้องวายุกำลังแปลภาษา, กรุณารอสักครู่ 😚"

        wait_msg = {"to": user_id, "messages": [{"type": "text", "text": text_mgs}]}
        self.line.push(data=json.dumps(wait_msg))
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.line.push(data=response.content)

    def post_ocr_translation(self, user_id, message_id): 
        url = self.configurator.get('api.translation.image')
        headers = { 'Content-Type': 'application/json'}
        payload = { 'message_id': message_id}
        text_mgs = "น้องวายุกำลังแปลภาษา, กรุณารอสักครู่ 😚"
        wait_msg = {"to": user_id, "messages": [{"type": "text", "text": text_mgs}]}
        self.line.push(data=json.dumps(wait_msg))
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        json_r = response.json()
        self.line.push(data=json.dumps({'to':user_id, 'messages':[json_r]}))

    def post_audio_translation(self): pass

    def post_interactive(self,type, event):
        user_id = event.source.user_id
        url = self.configurator.get('api.interactive')
        headers = { 'Content-Type': 'application/json'}
        
        if type == "keyword":
            payload = {
                'replyToken':event.reply_token,
                'type': 'postback', 
                'source': { 'type': 'user', 'userId': user_id },
                'postback': { 'data': 'keyword={}'.format(event.message.text) },
                'timestamp': { 'seconds': 0, 'nanos': 0 }
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            self.line.push(data=response.content)
        elif type == "postback":
            payload = {
                'replyToken':event.reply_token,
                'type': 'postback', 
                'source': { 'type': 'user', 'userId': user_id },
                'postback': { 'data': event.postback.data },
                'timestamp': { 'seconds': 0, 'nanos': 0 }
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            self.line.push(data=response.content)
            