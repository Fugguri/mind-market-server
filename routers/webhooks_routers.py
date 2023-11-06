from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from prisma_ import prisma
from prisma import models
from mics import utls
from mics.tg import TgBot
from aiogram.types import Message


webhooks_router = APIRouter()


@webhooks_router.post("/webhook/tg_bot/{bot_id}",  name="Получение сообщения", description="", tags=["webhooks"])
async def profile(bot_id: str, request: Request):
    tg_bot = await prisma.telegrambot.find_first(where={"id": bot_id})
    tg_provider: TgBot = TgBot(token=tg_bot.token)

    data = await request.json()
    print
    message = Message(data)
    print(message)
    print(message.text)
    tg_provider.bot.send_message(message.chat.id, message.text)
    # profile = await utls.check_profile_access_token(access_token, False)
    # return profile
