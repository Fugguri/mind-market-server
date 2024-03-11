from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .models import *
from sqlalchemy.orm import selectinload, lazyload, joinedload

from sqlalchemy.exc import IntegrityError


# CHATS FUNCTIONS

async def add_chat(session: AsyncSession, **kwargs):
    chat = Chat(**kwargs)
    session.add(chat)
    await session.commit()
    return chat


async def update_chat(session: AsyncSession, chat_id, **kwargs):
    chat = session.get(Chat, chat_id)
    for key, value in kwargs.items():
        setattr(chat, key, value)
    await session.commit()
    return chat


async def get_chat(session: AsyncSession, client_id, projectId):
    chat = await session.execute(select(Chat).filter(
        Chat.client_id == client_id and Chat.ProjectId == projectId))
    return chat.fetchone()
# TELEGTAM BOT FUNCTIONS


async def get_telegram_bot(session: AsyncSession, bot_id):
    bot = session.get(TelegramBot, bot_id)
    return bot


async def add_telegram_bot(session: AsyncSession, bot_data):
    new_bot = TelegramBot(**bot_data)
    session.add(new_bot)
    await session.commit()
    return new_bot


async def add_tg_bot(session: AsyncSession,
                     projectId,
                     assistantId,
                     botToken,
                     telegram_id,
                     first_name,
                     startMessage,
                     username,) -> TelegramBot:
    new_bot = TelegramBot()
    new_bot.id = str(uuid4())
    new_bot.projectId = projectId
    new_bot.assistantId = assistantId
    new_bot.botToken = botToken
    new_bot.telegram_id = telegram_id
    new_bot.first_name = first_name
    new_bot.username = username
    new_bot.startMessage = startMessage
    new_bot.createdAt = datetime.datetime.now()
    new_bot.updatedAt = datetime.datetime.now()
    session.add(new_bot)
    return new_bot
#  ---------------


async def get_tg_bot(session: AsyncSession, bot_id) -> TelegramBot:
    result = await session.execute(
        select(TelegramBot).filter(TelegramBot.id == bot_id))
    # session.refresh(result, "Project")
    return result.fetchone()


async def get_tg_bot_assistant(session: AsyncSession, assistant_id) -> TelegramBot:
    result = await session.execute(
        select(Assistant).where(Assistant.id == assistant_id))
    return result.fetchone()


async def add_tg_bot(session: AsyncSession,
                     projectId,
                     assistantId,
                     botToken,
                     telegram_id,
                     first_name,
                     startMessage,
                     username,) -> TelegramBot:
    new_bot = TelegramBot()
    new_bot.id = str(uuid4())
    new_bot.projectId = projectId
    new_bot.assistantId = assistantId
    new_bot.botToken = botToken
    new_bot.telegram_id = telegram_id
    new_bot.first_name = first_name
    new_bot.username = username
    new_bot.startMessage = startMessage
    new_bot.createdAt = datetime.datetime.now()
    new_bot.updatedAt = datetime.datetime.now()
    print(new_bot.botToken)

    session.add(new_bot)
    return new_bot


async def create_chat(session: AsyncSession,):
    new_chat = Chat()
    session.add(new_chat)


async def add_message(session: AsyncSession,
                      chat_id=None,
                      text=None,
                      files_url=None,
                      images_url=None,
                      incoming=None,
                      from_assistant=None,
                      from_user=None,
                      from_manager=None,
                      managerId=None,
                      assistant_id=None,
                      is_read=None,
                      timestamp=None,) -> TelegramBot:
    new_message = Message()
    new_message.id = str(uuid4())
    new_message.chat_id = chat_id
    new_message.text = text
    new_message.files_url = files_url
    new_message.images_url = images_url
    new_message.incoming = incoming
    new_message.from_assistant = from_assistant
    new_message.from_user = from_user
    new_message.from_manager = from_manager
    new_message.managerId = managerId
    new_message.assistant_id = assistant_id
    new_message.is_read = is_read
    new_message.timestamp = datetime.datetime.fromtimestamp(timestamp)
    new_message.createdAt = datetime.datetime.now()
    new_message.updatedAt = datetime.datetime.now()
    session.add(new_message)
    try:
        await session.commit()
    except IntegrityError as ex:
        session.rollback()
        print(ex)
    return new_message


async def get_client(session: AsyncSession, in_service_id: str = None, projectId=None,):
    result = await session.execute(select(Client).filter(
        Client.in_service_id == in_service_id and Client.ProjectId == projectId))
    return result.fetchone()


async def get_assistant(session: AsyncSession, assistantId: str = None,):
    result = await session.execute(
        select(Assistant).filter(Assistant.id == assistantId))
    return result.fetchone()


async def create_client_and_chat(session: AsyncSession,
                                 in_service_id: str = None,
                                 chatId=None,
                                 name=None,
                                 projectId=None,
                                 username=None,
                                 image_url=None,
                                 category=None,
                                 email=None,
                                 phone=None,
                                 about=None,
                                 companyName=None,
                                 tags=None,
                                 assistantId=None
                                 ):
    new_client = Client()
    new_client.id = str(uuid4())
    new_client.in_service_id = in_service_id
    new_client.chatId = chatId
    new_client.ProjectId = projectId
    new_client.name = name
    new_client.username = username
    new_client.image_url = image_url
    new_client.category = category
    new_client.email = email
    new_client.phone = phone
    new_client.about = about
    new_client.companyName = companyName
    new_client.tags = tags
    new_client.createdAt = datetime.datetime.now()
    new_client.updatedAt = datetime.datetime.now()

    new_chat = Chat()
    new_chat.assistant_id = assistantId
    new_chat.ProjectId = projectId
    new_chat.managerId = None
    new_chat.client_id = new_client.id
    new_chat.integrationId = None
    new_chat.is_blocked = False
    new_chat.is_assistant_in_chat = True
    new_chat.createdAt = datetime.datetime.now()
    new_chat.updatedAt = datetime.datetime.now()
    new_client.chatId = new_chat.id
    session.add(new_client)
    session.add(new_chat)
    try:
        await session.commit()
    except IntegrityError as ex:
        session.rollback()
        print(ex)
    return new_client, new_chat
