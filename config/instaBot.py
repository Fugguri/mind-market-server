from instabot import Bot
import dotenv 
from time import sleep 
import os
from DB.DB import Database
from mics._openai import create_responce
import asyncio 
import threading
class ReceiveMessages:
    
    
    
    def __init__(self) -> None :
        dotenv.load_dotenv()
        username = dotenv.get_key(".env","USERNAME")
        password = dotenv.get_key(".env","PASSWORD")
        self.bot = Bot()
        self.username = username
        self.password = password
        self.db = Database("test.db")
        self._create_response = create_responce
        self.bot.login(username = "gizzzar",
                       password = "Neskazu_1")


    def start_receive(self):

        # me = self.bot.get_user_info
        while True:
            mes = self.bot.get_messages()
            for a in mes["inbox"]["threads"]:
                income = False
                for d, value in a.items():
                    print(d,value)   
                    if d == "items":
                        if not value[0]["is_sent_by_viewer"]:
                            income = True
                        
                        user_id = value[0]["user_id"]
                        message_type = value[0]["item_type"]
                        last_message = value[0]["text"]
                    if d == "users":
                        # print(value)
                        username = value[0]["username"]
                        full_name = value[0]["full_name"]
                # print(user_id, username,full_name,last_message)
                if income:                        
                    print("receive")
                    response = self._create_response(user_id,last_message)
                    print("anser", response)
                    print(username)
                    self.bot.send_message(response,username)
                    
                else:
                    print("outcome")

                break
            sleep(3)

    
if __name__ == "__main__":
    bot = ReceiveMessages()
    bot.start_receive()