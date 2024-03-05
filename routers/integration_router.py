import asyncio
from sqlalchemy.exc import IntegrityError

from mics import jivo, tg, greenApi, utls
from models import schemas
from fastapi import APIRouter, HTTPException, Request, logger, Depends
from fastapi.logger import logger
from aiogram import types
from DB.db import AsyncSession, get_session
from DB.async_crud import add_tg_bot

integration_router = APIRouter()


@integration_router.post("/integrations/all/{projectId}", name="Список интеграции", description="Создание интеграции", tags=["Интеграции"])
async def create_tg_bot(projectId: str, request: Request, session: AsyncSession = Depends(get_session)):
    ...
    # Database.get_integration_by_project_id(projectId)


@integration_router.post("/integrations/tgbot", name="Добавление Telegram бота", description="Добавление бота, созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(tgbot: schemas.TgBotEntry, session: AsyncSession = Depends(get_session)):
    bot = tg.TgBot(tgbot.token)
    try:
        info = await bot.getInfo()
        me: types.User = info[0]
    except Exception as ex:
        return HTTPException(401, ex)
    await add_tg_bot(session=session,
                     telegram_id=me.id,
                     botToken=tgbot.token,
                     first_name=me.full_name,
                     username=me.username,
                     )
    try:

        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        print(ex)
        # raise Exception(f"The bot already stored")

    await bot.setWebhook(tgbot.token)
    # tg_bot_model = await db.get_telegrambot(bot_id=bot_id)
    # await messages.handle_telegrambot_message(json_request, tg_bot_model)


@integration_router.delete("/integrations/tgbot/{bot_id}", name="Удаление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, request: Request, session: AsyncSession = Depends(get_session)):
    ...


@integration_router.patch("/integrations/tgbot", name="Добавление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(tgbot: schemas.TgBotEntry, session: AsyncSession = Depends(get_session)):
    print(tgbot.assistantId)
    bot = tg.TgBot(tgbot.token)
    me: types.User = await bot.getInfo()
    print(me.as_json())
    # Database.create_tg_bot()
    # await bot.setWebhook(new.id)
    return "ghbdt"


@integration_router.post("/integrations/wabot/{access_token}", name="Добавление WhatsApp бота", description="Добавление профиля WhatsApp созданного в сервисе GreenApi", tags=["Интеграции"])
async def create_wa_bot(access_token: str, wabot: schemas.WaBotEntry, session: AsyncSession = Depends(get_session)):
    profile = await utls.check_profile_access_token(access_token)

    me = greenApi.Watsapp(wabot.IdInstance, wabot.ApiTokenInstance).get_me()
    # new = await prisma.whatsappbot.create(data={
    #     "phone": wabot.phone,
    #     "ApiTokenInstance": wabot.ApiTokenInstance,
    #     "IdInstance": wabot.IdInstance,
    #     'name': " ",
    #     'imageUrl': me,
    #     'profileId': profile.id,
    # })

    # return new


@integration_router.post("/integration/tguserbot/{access_token}", name="Новый ассистент", description="Создание нового ассистента", tags=["Интеграции"])
async def create_tg_user_bot(access_token: str, tguserbot: schemas.TgUserBotEntry, session: AsyncSession = Depends(get_session)):
    profile = await utls.check_profile_access_token(access_token)

    # new = await prisma.telegrambot.create(data={
    #     "token": tguserbot.token,
    #     'telegram_id': str(me[0].id),
    #     'name': me[0].first_name,
    #     'imageUrl': me[1],
    #     'profileId': user.id,
    # })

    return profile


@integration_router.post("/integration/instagram/webhook", description="Регистрация instagram webhook", tags=["Системные"])
async def user(request: Request, session: AsyncSession = Depends(get_session)):
    body = await request.body()

    print(body)
    return


@integration_router.get("/integration/instagram/webhook", description="Регистрация instagram webhook", tags=["Системные"])
async def user(request: Request, session: AsyncSession = Depends(get_session)):
    res = request.query_params.get('hub.challenge')
    return int(res)


@integration_router.post("/integration/jivo/{id}", name="JivoBot запрос ответа", description="Запрос ответа от ассистента", tags=["Интеграции"])
async def create_user(id: str, request: schemas.ClientMessage, session: AsyncSession = Depends(get_session)):
    match request.event:
        case "CHAT_CLOSED":
            return
        case "INVITE_AGENT":
            return
        case "AGENT_JOINED":
            return
        case "AGENT_UNAVAILABLE":
            return
        case "CLIENT_INFO":
            return
        case _:
            pass
    # bot = await Database.get_jivo_bot(id)

    response = await jivo.create_jivo_responce(request, bot.assistant)
    answer_request = await jivo.send_jivo_aswer(response, bot.provider_id, bot.assistant_id)

    if answer_request.status_code == 200:
        ...
        # обновить счетчик ответов
    elif answer_request.status_code == 400:
        await tg.tg_bot.send_err_notification(answer_request.json())
    elif answer_request.status_code == 500:
        await tg.tg_bot.send_err_notification(answer_request.json())

    return response.__dict__
# print(asyncio.run(Database.get_jivo_bot(
#     jivo_id="59e250a4-f1d4-4585-8141-d35d3cb1736")))
