from fastapi import APIRouter, Path, Query, Request, HTTPException

from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message
from mics._openai import create_response

webhooks_router = APIRouter()


@webhooks_router.post("/webhook/tgbot/{bot_id}",  name="Получение сообщения от телеграмм", description="", tags=["webhooks"])
async def profile(bot_id: str, request: Request):
    print(bot_id)
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
