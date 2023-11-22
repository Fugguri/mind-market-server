from mics import jivo, tg, greenApi, utls
from prisma_ import prisma
from models import schemas
from fastapi import APIRouter, HTTPException, Request, logger
from fastapi.logger import logger

from prisma import models


integration_router = APIRouter()


@integration_router.post("/integrations/tgbot/{bot_id}", name="webhook для telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(bot_id: str, request: Request):
    req = await request.json()
    message = req.get("message")
    if not message:
        return
    sender = message.get("from")
    chat = message.get("chat")
    text = message.get("text")
    if text:
        print(text)


@integration_router.delete("/integrations/tgbot/{bot_id}", name="webhook для telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, request: Request):
    req = await request.json()
    message = req.get("message")
    if not message:
        return
    sender = message.get("from")
    chat = message.get("chat")
    text = message.get("text")
    if text:
        print(text)


@integration_router.patch("/integrations/tgbot/{user_id}", name="Добавление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, tgbot: schemas.TgBotEntry):

    bot = tg.TgBot(tgbot.token)
    me = await bot.getInfo()
    new = await prisma.telegrambot.create(data={
        "token": tgbot.token,
        'telegram_id': str(me[0].id),
        'name': me[0].first_name,
        "assistantId": tgbot.assistantId,
        'imageUrl': me[1],
        'userId': user_id,
    })
    await bot.setWebhook(new.id)
    return new


@integration_router.post("/integrations/wabot/{access_token}", name="Добавление WhatsApp бота", description="Добавление профиля WhatsApp созданного в сервисе GreenApi", tags=["Интеграции"])
async def create_wa_bot(access_token: str, wabot: schemas.WaBotEntry):
    profile = await utls.check_profile_access_token(access_token)

    me = greenApi.Watsapp(wabot.IdInstance, wabot.ApiTokenInstance).get_me()
    new = await prisma.whatsappbot.create(data={
        "phone": wabot.phone,
        "ApiTokenInstance": wabot.ApiTokenInstance,
        "IdInstance": wabot.IdInstance,
        'name': " ",
        'imageUrl': me,
        'profileId': profile.id,
    })

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


@integration_router.post("/integration/jivo/{access_token}", name="JivoBot запрос ответа", description="Запрос ответа от ассистента", tags=["Интеграции"])
async def create_user(access_token: str, request: schemas.ClientMessage):
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

    assistant = await utls.check_assistant_access_token(access_token)
    logger.debug(request.model_dump_json())

    response = await jivo.create_jivo_responce(request, assistant)
    answer_request = await jivo.send_jivo_aswer(response, assistant)
    print(answer_request.json())
    if answer_request.status_code == 200:
        post = await prisma.assistant.update(
            where={
                'id': assistant.id,
            },
            data={
                'use_count': {
                    'increment': 1,
                },
            },
        )
    elif answer_request.status_code == 400:
        await tg.tg_bot.send_err_notification(answer_request.json())
    elif answer_request.status_code == 500:
        await tg.tg_bot.send_err_notification(answer_request.json())

    return response.__dict__
