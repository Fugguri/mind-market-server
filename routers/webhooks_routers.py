from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from prisma_ import prisma
from prisma import models
from mics import utls
from mics.tg import TgBot


webhooks_router = APIRouter()


@webhooks_router.post("/webhook/tg_bot/{bot_id}", response_model=models.Profile, name="Данные профиля", description="Данные по пользователе", tags=["Профиль"])
async def profile(bot_id: str, request: Request):
    tg_bot = await prisma.telegrambot.find_first(where={"id": bot_id})
    tg_provider: TgBot = TgBot(token=tg_bot.token)

    message: TgBot.types.Message = TgBot.types.Message(await request.json())
    print(message.text)
    tg_provider.bot.send_message(message.chat.id, message.text)
    # profile = await utls.check_profile_access_token(access_token, False)
    return profile