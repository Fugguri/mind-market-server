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
        result = await client.post(url=url, headers=headers, data=json)
    if result.is_client_error:
        print(json)
        print(result.status_code)
        print(result.content)
    return result


{"id": "996344da-d8f4-11ec-9aaf-c5bde7170335",
    "event": "BOT_MESSAGE",
    "message":
    {"type": "TEXT",
     "text": "Конечно, я готов вам помочь. Какой у вас вопрос?",
     "timestamp": 1653127681833},
    "client_id": "3209", "chat_id": "4209"
 }
{"id": "2bc2f2c2-e5b8-11ee-91b4-b758e91cf880",
    "event": "BOT_MESSAGE"
    "message": 
    {"type": "TEXT", 
     "text": "Привет! Как я могу помочь тебе с услугами по внедрению искусственного интеллекта?", 
     "timestamp": 1710828966}, 
    "client_id": "2", "chat_id": "28", 
 }
