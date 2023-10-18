import requests
from models import schemas
from mics._openai import create_responce
from prisma import models


async def create_jivo_responce(request: schemas.ClientMessage, assistant: models.Assistant) -> schemas.BotMessage:

    response = schemas.BotMessage(**request.dict())
    response.event = "BOT_MESSAGE"
    response.message.text = await create_responce(request.chat_id, assistant.settings, request.message.text)

    return response


async def send_jivo_aswer(response: schemas.BotMessage, assistant: models.Assistant):

    url = f"https://bot.jivosite.com/webhooks/{assistant.jivoBot[0].provider_id}/{assistant.token}"
    json = response.dict()
    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, headers=headers, json=json)

    return result
