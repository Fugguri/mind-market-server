from mics import jivo, tg, greenApi, utls
from models import schemas
from fastapi import APIRouter, HTTPException, Request, logger
from fastapi.logger import logger

from mics._openai import create_response
from providers import db, messages


integration_router = APIRouter()


@integration_router.post("/integrations/tgbot/{bot_id}", name="webhook для telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(bot_id: str, request: Request):
    json_request = await request.json()
    print(json_request)
    tg_bot_model = await db.get_telegrambot(bot_id=bot_id)
    await messages.handle_telegrambot_message(json_request, tg_bot_model)


@integration_router.delete("/integrations/tgbot/{bot_id}", name="Удаление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, request: Request):
    ...


@integration_router.patch("/integrations/tgbot/{user_id}", name="Добавление telegram бота", description="Добавление бота созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(user_id: str, tgbot: schemas.TgBotEntry):

    bot = tg.TgBot(tgbot.token)
    me = await bot.getInfo()

    # await bot.setWebhook(new.id)
    # return new


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

    response = await jivo.create_jivo_responce(request, assistant)

    answer_request = await jivo.send_jivo_aswer(response, assistant)

    if answer_request.status_code == 200:
        ...
        # обновить счетчик ответов
    elif answer_request.status_code == 400:
        await tg.tg_bot.send_err_notification(answer_request.json())
    elif answer_request.status_code == 500:
        await tg.tg_bot.send_err_notification(answer_request.json())

    return response.__dict__
