from fastapi import APIRouter, HTTPException, Request, logger, Depends
from aiogram import types
from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message
from mics._openai import create_response
from DB.db import AsyncSession, get_session
from DB.async_crud import get_tg_bot
webhooks_router = APIRouter()

bots = dict()


@webhooks_router.post("/webhooks/tgbot/{bot_id}",  name="Получение сообщения от телеграмм", description="", tags=["webhooks"])
async def profile(bot_id: str, request: Request, session: AsyncSession = Depends(get_session)):
    telegram = await get_tg_bot(session, bot_id)[0]
    print(telegram)
    req = await request.json()
    tg_bot = TgBot(telegram.botToken)
    print(req)
    message = req.get("message")
    if not message:
        return
    sender = message.get("from_user").get("id")
    chat = message.get("chat")
    text = message.get("text")
    if text:
        print(text)

    # response = create_response(user_id="", settings="", text=text)
    # await tg_bot.answer(text, settings, sender,)
