import httpx
from models import schemas
from mics._openai import create_response


async def create_jivo_responce(request: schemas.ClientMessage, assistant) -> schemas.BotMessage:

    response = schemas.BotMessage(**request.dict())
    response.event = "BOT_MESSAGE"
    response.message.text = await create_response(request.chat_id, assistant.settings, request.message.text)

    return response


async def send_jivo_aswer(response_model: schemas.BotMessage, provider_id: str, ptoject_id: str):

    url = f"https://bot.jivosite.com/webhooks/{provider_id}/{ptoject_id}"
    json = response_model.model_dump_json()

    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, data=json)
        # print(json)
        print(response.status_code)
        print(response.content)
    return response
