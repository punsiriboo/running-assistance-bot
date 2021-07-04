import json
import requests
from system import Configurator


class LineResponse:

    def __init__(self, config: Configurator):
        self.configurator = config
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.configurator.get('line.access_token'))
        }

    def push(self, data): 
        url = 'https://api.line.me/v2/bot/message/push'
        response = requests.post(url, data = data, headers=self.headers)
