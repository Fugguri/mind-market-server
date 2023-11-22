from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from prisma_ import prisma
from prisma import models
from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message


webhooks_router = APIRouter()


@webhooks_router.post("/webhook/tg_bot/{bot_id}",  name="Получение сообщения", description="", tags=["webhooks"])
async def profile(bot_id: str, request: Request):
    print(request.json())

    # tg_bot = await prisma.telegrambot.find_first(where={"id": bot_id}, include={"assistant": True})
    # tg_provider: TgBot = TgBot(token=tg_bot.token)

    # data = await request.json()

    # message = data.get("message")
    # user_id = message.get("from").get("id")
    # text = message.get("text")
    # response = await _openai.create_responce(
    #     user_id, tg_bot.assistant.settings, text)

    # await tg_provider.bot.send_message(user_id, response)
    # # profile = await utls.check_profile_access_token(access_token, False)
    # # return profile
