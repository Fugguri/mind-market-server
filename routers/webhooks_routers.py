from fastapi import APIRouter, Path, Query, Request, HTTPException
from aiogram import types
from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message
from mics._openai import create_response

webhooks_router = APIRouter()


@webhooks_router.post("/webhooks/tgbot/{bot_id}",  name="Получение сообщения от телеграмм", description="", tags=["webhooks"])
async def profile(bot_id: str, message: types.Message):
    print(bot_id)
    print(message)
    # create_response(user_id="", settings="", text=text)
