from aiogram import Bot, Dispatcher, executor, types

import asyncio


class TgBot:

    def __init__(self, token=None) -> None:

        self.bot: Bot = Bot(token=token)
        self.dispather: Dispatcher = Dispatcher(bot=self.bot)
        self.executor = executor
        self.types: types = types

    async def getInfo(self) -> [types.User, str]:
        self.dispather.start_polling()

        me = await self.bot.get_me()
        pict = await self.bot.get_user_profile_photos(me.id)
        file = await self.bot.get_file(file_id=pict.photos[0][0].file_id)
        url = self.bot.get_file_url(file_path=file)
        self.dispather.stop_polling()

        return [me, url]


class TgUserBot:
    pass
