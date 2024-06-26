from fastapi import BackgroundTasks
import asyncio
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from mics import jivo, tg, greenApi, utls
from models import schemas
from fastapi import APIRouter, HTTPException, Request, logger, Depends
from fastapi.responses import HTMLResponse
from fastapi.logger import logger
from aiogram import types
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from DB.db import get_session
from DB.async_crud import add_tg_bot, get_jivo_bot, get_assistant, create_jivo_bot
from services.scheduler import message_scheduler, async_message_scheduler
integration_router = APIRouter()


@integration_router.post("/integrations/all/{projectId}", name="Список интеграции", description="Создание интеграции", tags=["Интеграции"])
async def create_tg_bot(projectId: str, request: Request, session: AsyncSession = Depends(get_session)):
    ...
    # Database.get_integration_by_project_id(projectId)


@integration_router.post("/integrations/tgbot", name="Добавление Telegram бота", description="Добавление бота, созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(tgbot: schemas.TgBotEntry, session: AsyncSession = Depends(get_session)):
    bot = tg.TgBot(tgbot.botToken)
    print(tgbot.botToken)
    try:
        info = await bot.getInfo()
        print(info)
        me: types.User = info
    except Exception as ex:
        print(ex)
        return HTTPException(401, ex)

    new_bot = await add_tg_bot(session=session,
                               projectId=tgbot.projectId,
                               assistantId=tgbot.assistantId,
                               telegram_id=me.id,
                               botToken=tgbot.botToken,
                               first_name=me.full_name,
                               username=me.username,
                               startMessage=tgbot.startMessage
                               )

    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        print(ex)
        # raise Exception(f"The bot already stored")

    await bot.setWebhook(new_bot.id, new_bot.botToken)


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


@integration_router.post("/integration/jivo", name="JivoBot запрос ответа", description="Запрос ответа от ассистента", tags=["Интеграции"])
async def create_user(jivoBot: schemas.JivoBotEntry, session: AsyncSession = Depends(get_session)):
    bot = await create_jivo_bot(session, jivoBot)


@integration_router.post("/integration/jivo/{project_id}", name="JivoBot запрос ответа", description="Запрос ответа от ассистента", tags=["Интеграции"])
async def create_user(project_id: str, request: schemas.ClientMessage, session: AsyncSession = Depends(get_session), background_task: BackgroundTasks = BackgroundTasks):
    # await create_jivo_answer(project_id, request, session)
    background_task.add_task(run_async,
                             #    replace_existing=True,
                             #   trigger='date',
                             #    run_date=remaining_datetime,
                             #   id=str(request.id),
                             #   name=str(request.id),
                             project_id, request, session)

    return HTMLResponse(status_code=200)

    # if answer_request.status_code == 200:
    #     ...
    #     # обновить счетчик ответов
    # elif answer_request.status_code == 400:
    #     await tg.tg_bot.send_err_notification(answer_request.json())
    # elif answer_request.status_code == 500:
    #     await tg.tg_bot.send_err_notification(answer_request.json())


def run_async(project_id: str, request: schemas.ClientMessage, session: AsyncSession = Depends(get_session)):
    asyncio.run(create_jivo_answer(project_id, request, session))


async def create_jivo_answer(project_id: str, request: schemas.ClientMessage, session: AsyncSession = Depends(get_session)):
    print(request.json())
    print(datetime.now())
    print("start")
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
            print(request.event)
            pass
    jivo_ = await get_jivo_bot(session, project_id)
    print("got jivo bot")

    print(jivo_)
    if not jivo_:
        print("error")
        return HTMLResponse(content="User doesn't exist", status_code=400)
    assistant = await get_assistant(session, jivo_[0].assistant_id)
    print("got assistant")

    response = await jivo.create_jivo_responce(request, assistant[0])
    print("create responce")

    await jivo.send_jivo_aswer(response, jivo_[0].provider_id, project_id)
    print("send answer")
