import requests
import os


class Telegram:
    def __init__(self):
        self.api_key = os.environ["TELEGRAM_API_KEY"]
        self.url = "https://api.telegram.org/bot{}/sendMessage".format(
            self.api_key)

    def send_message(self, text_message, chat_id="-1001860660149"):
        '''
        Send message to a telegram channel

        :params text_message: The message to send.
        :params chat_id: The chat id of the channel to send the message to.
        :return: None
        '''
        payload = {
            "chat_id": chat_id,
            "text": f"{text_message}",
            "parse_mode": "Markdown",
        }
        try:
            requests.get(self.url, params=payload)
        except:
            pass
        return True
