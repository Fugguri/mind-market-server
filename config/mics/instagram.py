
import logging
from instagrapi import Client
from instagrapi.types import DirectThread
from instagrapi.exceptions import LoginRequired
logger = logging.getLogger()
import dotenv
from time import sleep
# from ..DB import Database
from mics._openai import create_responce
import os
username = dotenv.get_key(".env","USERNAME")
password = dotenv.get_key(".env","PASSWORD")
class ReceiveMessages:
    
    
    
    def __init__(self) -> None :
        dotenv.load_dotenv()
        username = dotenv.get_key(".env","USERNAME")
        password = dotenv.get_key(".env","PASSWORD")
        self.bot:Client = Client()
        self.username = username
        self.password = password
        # self.bot.set_proxy(dsn="https://45.92.171.19:8000:dGC5o8:zcf7tx")
        # self.db = Database("test.db")
        self._create_response = create_responce
        self.bot.delay_range = [5, 20]


    def _answer_messages(self,messages:tuple[DirectThread]|list[DirectThread]):
        for message in messages:
            income= False
            m = message.messages[0] 
            u = message.users[0]
            if not m.is_sent_by_viewer:
                income = True
            user_id = m.user_id
            message_type = m.item_type
            last_message = m.text
            username = u.username
            full_name = u.full_name
            if income:
                if message_type == "text":        
                    response = self._create_response(user_id,last_message)
                    self.bot.direct_send_seen(m.thread_id)
                    self.bot.direct_send(response,[m.user_id,])
                else:
                    print("Send is not text")

    def _login(self,clear=False):
        if clear:
            os.remove(path)
        path = f"{os.path.dirname(os.path.abspath(__file__))}/dump.json"
        self.bot.load_settings(path)
        self.bot.login(username = "gazzzur",
                        password = "Neskazu1")
        # try:
        # except:
        #     self.bot.login(username="gazzzur", password="Neskazu1", relogin=True)
        # finally:            
        #     self.bot.dump_settings(path)
        #     self.bot.login(username = "gazzzur",
        #                 password = "Neskazu1")
    def start_receive(self):
        self._login()
        while True:
            # try:
                pending_messages = self.bot.direct_pending_inbox()
                if pending_messages:
                    self._answer_messages(pending_messages)
                messages = self.bot.direct_threads(amount=30,selected_filter="unread",thread_message_limit=1)
                if messages:
                    self._answer_messages(messages)
            # except LoginRequired:
            #     sleep(10)
            #     print("relogin")
            #     self._login(True)
            # except Exception as ex :
            #     print(ex)    
                # sleep(10)

    
if __name__ == "__main__":
    bot = ReceiveMessages()
    while True:
        try:
            print("Запускаю бота")
            bot.start_receive()
        except KeyboardInterrupt:
            print("stopping")
            break
        # except Exception as ex:
        #     print(ex)
