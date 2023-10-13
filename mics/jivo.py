from models import schemas
from mics._openai import create_responce
import requests

async def create_jivo_responce(request:schemas.ClientMessage, ) -> schemas.BotMessage: 
    pass
    # response = schemas.BotMessage(**request.dict())
    # response.event = "BOT_MESSAGE"
    # response.message.text = await create_responce(request.chat_id,user.assistants[0].settings, request.message.text)
    
    # return response


async def send_jivo_aswer(response:schemas.BotMessage):
    pass
    # url = f"https://bot.jivosite.com/webhooks/{user.provider_id}/{user.token}"
    # json = response.dict()
    # headers  = {"Content-Type": "application/json"}
    # result = requests.post(url=url,headers=headers ,json=json)
    
    # return result