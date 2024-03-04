import asyncio
from mics import jivo, tg, greenApi, utls
from models import schemas
from fastapi import APIRouter, HTTPException, Request, logger
from fastapi.logger import logger
from aiogram import types
from mics._openai import create_response
from providers import db, messages
from DB import db as Database

integration_router = APIRouter()


@integration_router.post("/integrations/{user_id}", name="Создание интеграции", description="Создание интеграции", tags=["Интеграции"])
async def create_tg_bot(user_id: str, request: Request):
    print(request)


@integration_router.post("/integrations/tgbot/{bot_id}", name="webhook для telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(bot_id: str, request: Request):
    json_request = await request.json()
    tg_bot_model = await db.get_telegrambot(bot_id=bot_id)
    await messages.handle_telegrambot_message(json_request, tg_bot_model)


@integration_router.delete("/integrations/tgbot/{bot_id}", name="Удаление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, request: Request):
    ...


@integration_router.patch("/integrations/tgbot", name="Добавление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(tgbot: schemas.TgBotEntry):
    print(tgbot)
    bot = tg.TgBot(tgbot.token)
    me: types.User = await bot.getInfo()
    print(me.as_json())
    # Database.create_tg_bot()
    # await bot.setWebhook(new.id)
    return "ghbdt"


@integration_router.post("/integrations/wabot/{access_token}", name="Добавление WhatsApp бота", description="Добавление профиля WhatsApp созданного в сервисе GreenApi", tags=["Интеграции"])
async def create_wa_bot(access_token: str, wabot: schemas.WaBotEntry):
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

    return new


@integration_router.post("/integration/tguserbot/{access_token}", name="Новый ассистент", description="Создание нового ассистента", tags=["Интеграции"])
async def create_tg_user_bot(access_token: str, tguserbot: schemas.TgUserBotEntry):
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
async def user(request: Request):
    body = await request.body()

    print(body)
    return


@integration_router.get("/integration/instagram/webhook", description="Регистрация instagram webhook", tags=["Системные"])
async def user(request: Request):
    res = request.query_params.get('hub.challenge')
    return int(res)


@integration_router.post("/integration/jivo/{id}", name="JivoBot запрос ответа", description="Запрос ответа от ассистента", tags=["Интеграции"])
async def create_user(id: str, request: schemas.ClientMessage):
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
    from DB.database import JivoBot
    bot: JivoBot = await Database.get_jivo_bot(id)

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
