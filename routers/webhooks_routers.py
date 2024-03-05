from fastapi import APIRouter, HTTPException, Request, logger, Depends
from aiogram import types
from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message
from mics._openai import create_response
from DB.db import AsyncSession, get_session
from DB.async_crud import get_tg_bot, get_tg_bot_assistant, Assistant, TelegramBot
webhooks_router = APIRouter()

bots = dict()


@webhooks_router.post("/webhooks/tgbot/{bot_id}",  name="Получение сообщения от телеграмм", description="", tags=["webhooks"])
async def profile(bot_id: str, request: Request, session: AsyncSession = Depends(get_session)):
    telegram: TelegramBot = await get_tg_bot(session, bot_id)
    assistant: Assistant = await get_tg_bot_assistant(session, telegram.assistantId)
    print(telegram)
    req = await request.json()
    tg_bot = TgBot(telegram.botToken)
    print(req)
    message = req.get("message")
    if not message:
        return
    sender = message.get("from").get("id")
    text = message.get("text")
    if text == "/start":
        await tg_bot.sendMessage(sender, telegram.startMessage)
        return
    chat = message.get("chat")
    if text:
        print(text)

    # response = await create_response(
    #     user_id=sender, settings=assistant.settings, text=text)
    await tg_bot.answer(text, sender, assistant.settings)
