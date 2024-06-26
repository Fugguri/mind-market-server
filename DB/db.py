import dotenv
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_async_engine(
    DATABASE_URL, poolclass=NullPool, echo=False, pool_pre_ping=True, pool_recycle=3600)
# if not database_exists(engine.url):
#     create_database(engine.url)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


engine = create_engine(DATABASE_URL,  poolclass=NullPool,
                       pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         await db.close()


async def get_session() -> AsyncSession:
    try:
        async with async_session() as session:
            try:
                yield session
            except:
                await session.close()
    except:
        pass

# async def init_models():
#     async with engine.begin() as conn:

#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
