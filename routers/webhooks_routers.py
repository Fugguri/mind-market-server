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
    print(await get_tg_bot(session, bot_id))
    req = await request.json()
    print(req)
    message = req.get("message")
    if not message:
        return
    sender = message.get("from")
    chat = message.get("chat")
    text = message.get("text")
    if text:
        print(text)

    create_response(user_id="", settings="", text=text)
