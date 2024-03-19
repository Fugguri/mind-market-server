import requests
from models import schemas
from mics._openai import create_response
from httpx import AsyncClient


async def create_jivo_responce(request: schemas.ClientMessage, assistant) -> schemas.BotMessage:

    response = schemas.BotMessage(**request.dict())
    response.event = "BOT_MESSAGE"
    response.message.text = await create_response(request.chat_id, assistant.settings, request.message.text)

    return response


async def send_jivo_aswer(response: schemas.BotMessage, provider_id: str, ptoject_id: str):

    url = f"https://bot.jivosite.com/webhooks/{provider_id}/{ptoject_id}"
    json = response.json()

    headers = {"Content-Type": "application/json"}
    async with AsyncClient() as client:
        result = await client.post(url=url, headers=headers, content=json)
    if result.is_client_error:
        print(json)
        print(result.status_code)
        print(result.headers)
    return result
