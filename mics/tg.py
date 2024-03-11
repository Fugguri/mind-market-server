import asyncio
from aiogram import Bot, Dispatcher, executor, types
from mics._openai import create_response
import requests


class TgUserBot:
    pass


class TgBot:

    def __init__(self, token=None) -> None:

        self.bot: Bot = Bot(token=token)
        self.dispather: Dispatcher = Dispatcher(bot=self.bot)
        self.executor = executor
        self.types: types = types
        self.BASE_WEBHOOK_URL = "https://web-mindmarket.ru/api_v2/webhooks/tgbot/"

    async def getInfo(self) -> [types.User, str]:
        me = await self.dispather.bot.get_me()

        # pict = await self.dispather.bot.get_user_profile_photos(me.id)
        # file = await self.dispather.bot.get_file(file_id=pict.photos[0][0].file_id)

        # url = self.bot.get_file_url(file_path=file)
        await self.bot.close()
        return url

    async def setWebhook(self, bot_id: str) -> str:
        print(self.BASE_WEBHOOK_URL + bot_id)
        url = f'https://api.telegram.org/bot5489223512:AAGNP0Bc3uHprsQxv8HMVHjfGjlIFiuXVKE/setWebhook?url=https://web-mindmarket.ru/api_v2/webhooks/tgbot/{bot_id}'
        requests.get(url)
        return await self.bot.set_webhook(url=self.BASE_WEBHOOK_URL + bot_id)

    async def answer(self, text, sender_id, settings) -> str:

        if text:
            response = await create_response(sender_id, settings, text)
            mes = await self.sendMessage(sender_id, response)
        return response

    async def sendMessage(self, receiver_id: str | int, text: str) -> str:

        return await self.dispather.bot.send_message(chat_id=receiver_id, text=text)

    async def stop(self):
        self.dispather.stop_polling()


if __name__ == "__main__":
    ...
