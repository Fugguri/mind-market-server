import asyncio
from aiogram import Bot, Dispatcher, executor, types
from mics._openai import create_response


class TgUserBot:
    pass


class TgBot:

    def __init__(self, token=None) -> None:

        self.bot: Bot = Bot(token=token)
        self.dispather: Dispatcher = Dispatcher(bot=self.bot)
        self.executor = executor
        self.types: types = types
        self.BASE_WEBHOOK_URL = "web-mindmarket.ru/api_v2/integrations/tgbot/"

    async def getInfo(self) -> [types.User, str]:
        me = await self.bot.get_me()

        pict = await self.bot.get_user_profile_photos(me.id)
        file = await self.bot.get_file(file_id=pict.photos[0][0].file_id)

        url = self.bot.get_file_url(file_path=file)

        return [me, url]

    async def setWebhook(self, bot_id: str) -> str:

        return await self.bot.set_webhook(url=self.BASE_WEBHOOK_URL + bot_id)

    async def answer(self, text, sender_id, settings):

        if text:
            response = await create_response(sender_id, settings, text)
            return await self.sendMessage(sender_id, response)

    async def sendMessage(self, receiver_id: str | int, text: str) -> str:

        return await self.bot.send_message(chat_id=receiver_id, text=text)


if __name__ == "__main__":
    ...
