import requests
from models import schemas
from mics._openai import create_response


async def create_jivo_responce(request: schemas.ClientMessage, assistant) -> schemas.BotMessage:

    response = schemas.BotMessage(**request.dict())
    response.event = "BOT_MESSAGE"
    response.message.text = await create_response(request.chat_id, assistant.settings, request.message.text)

    return response


async def send_jivo_aswer(response: schemas.BotMessage, provider_id: str, jivo_id: str):

    url = f"https://bot.jivosite.com/webhooks/{assistant.jivoBot[0].provider_id}/{assistant.token}"
    json = response.model_dump_json()
    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, headers=headers, json=json)

    return result
