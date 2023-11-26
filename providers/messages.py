from prisma import models
from mics import jivo, tg, greenApi, utls
from aiogram.types import Message
from providers import db


async def handle_telegrambot_message(json_request,
                                     tg_bot_model: models.TelegramBot):
    TGBot = tg.TgBot(tg_bot_model.token)

    mes = Message(**json_request.get("message"))

    message = json_request.get("message")
    sender = message.get("from")
    sender_id = sender.get("id")
    chat = message.get("chat")
    text = message.get("text")

    client = await db.get_client(sender_id)
    if not client:
        client = await db.create_client(
            name=mes.from_user.full_name,
            username=mes.from_user.username,
            InChannelId=mes.from_user.id,
            userId=str(tg_bot_model.userId)
        )
    chat = await db.get_chat()
    if not chat:
        chat = await db.create_chat(
            models.enums.ChannelType.TelegramBot,
            tg_bot_model.userId,
            tg_bot_model.assistantId
        )
    await db.create_message(text, chat.id)
    if message:
        await TGBot.answer(text, sender_id, tg_bot_model.assistant.settings)
