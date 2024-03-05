from fastapi import APIRouter, HTTPException, Request, logger, Depends
from aiogram import types
from mics import utls, _openai
from mics.tg import TgBot
from aiogram.types import Message
from models import schemas
from mics._openai import create_response
from DB.db import AsyncSession, get_session
from DB.async_crud import get_tg_bot, get_tg_bot_assistant, Assistant, TelegramBot, Chat, Client, get_client, get_chat, add_message, create_client_and_chat, get_assistant
webhooks_router = APIRouter()

bots = dict()


@webhooks_router.post("/webhooks/tgbot/{bot_id}",  name="Получение сообщения от телеграмм", description="", tags=["webhooks"])
# async def profile(bot_id: str, message: schemas.TgBotMessageEntry, session: AsyncSession = Depends(get_session)):
async def profile(bot_id: str, req=Request):
    print(req.values)
    # if not message.message.text:
    #     return

    # telegram: TelegramBot = await get_tg_bot(session, bot_id)
    # telegram: TelegramBot = telegram[0]
    # projectId = telegram.projectId
    # assistant: Assistant = await get_assistant(session=session, assistantId=telegram.assistantId)

    # client: Client = await get_client(session=session,
    #                                   projectId=telegram.projectId,
    #                                   in_service_id=message.message.from_.id,
    #                                   )

    # if not client:
    #     client_and_chat = await create_client_and_chat(session=session, in_service_id=message.message.from_.id,
    #                                                    name=message.message.from_.first_name,
    #                                                    projectId=telegram.projectId,
    #                                                    username=message.message.from_.username,
    #                                                    assistantId=telegram.assistantId,)
    #     client = client_and_chat[0]
    #     chat: Chat = client_and_chat[1]
    # else:
    #     client: Client = client[0]
    #     chat: Chat = await get_chat(session=session, client_id=client.id, projectId=projectId,)

    # tg_bot = TgBot(telegram.botToken)
    # await add_message(session=session,
    #                   text=message.message.text,
    #                   chat_id=chat[0].id,
    #                   incoming=True,
    #                   from_assistant=False,
    #                   from_user=False,
    #                   from_manager=False,
    #                   assistant_id=telegram.assistantId,
    #                   is_read=False,
    #                   timestamp=message.message.date,)
    # if message.message.text == "/start":
    #     await tg_bot.sendMessage(message.message.from_.id, telegram.startMessage)
    #     return

    # print(text)
    # # response = await create_response(
    # #     user_id=sender, settings=assistant.settings, text=text)
    # await tg_bot.answer(message.message.text, message.message.from_.id, assistant[0].settings)
