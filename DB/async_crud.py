from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *
from sqlalchemy.exc import IntegrityError


async def checker(func):
    async def _wrapper(session, *args, **kwargs):
        try:
            await func(session, *args, **kwargs)
            await session.commit()
        except IntegrityError as ex:
            await session.rollback()
            print(ex)
            raise Exception(f"The {args} already stored")
    return _wrapper


# @checker
async def get_tg_bot(session: AsyncSession, bot_id) -> TelegramBot:
    result = await session.execute(select(TelegramBot).where(id=bot_id))
    return result


# @checker
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
