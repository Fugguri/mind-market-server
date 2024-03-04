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
async def add_tg_bot(session: AsyncSession, **kwargs) -> TelegramBot:
    new_city = TelegramBot(kwargs)
    session.add(new_city)
    return new_city
