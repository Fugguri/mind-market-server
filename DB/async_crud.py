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
# async def get_biggest_cities(session: AsyncSession) -> list[City]:
#     result = await session.execute(select(City).order_by(City.population.desc()).limit(20))
#     return result.scalars().all()


# @checker
async def add_tg_bot(session: AsyncSession,
                     botToken,
                     telegram_id,
                     first_name,
                     username,) -> TelegramBot:
    new_bot = TelegramBot()
    new_bot.botToken = botToken,
    new_bot.telegram_id = telegram_id,
    new_bot.first_name = first_name,
    new_bot.username = username
    session.add(new_bot)
    return new_bot
