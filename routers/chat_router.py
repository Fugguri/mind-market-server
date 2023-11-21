from mics._openai import create_response

from models import *
from fastapi import APIRouter, Path, Query, Request, HTTPException, Depends
from typing import Annotated
from models import schemas
from sqlalchemy.orm import Session
from datetime import datetime
import requests
from prisma import models


chat_router = APIRouter()


# @a_router.post("/asistant/{token}", name="Ассистент",description="Запрос ответа от ассистента",tags=["Ассистент"])
# async def create_user(token: Annotated[str, Path(title="user access token")],
#                       request: schemas.ClientMessage,
#                       db: Session = Depends(get_db)):

#     verify: models.Users = crud.verify_token(db, token)

#     if not verify:
#         raise HTTPException(status_code=404, detail="Invalin token")

#     is_pay = verify.expires >= datetime.now()

#     if not is_pay:
#         raise HTTPException(status_code=404, detail="Your access token is expired. Contact with us to pay for access.")
#     # if request.event == :
#     response = schemas.BotMessage(**request.dict())
#     response.event = "BOT_MESSAGE"
#     response.message.type = "TEXT"
#     response.message.timestamp = datetime.timestamp(datetime.now())
#     response.message.text = await create_response(request.chat_id,verify.assistants[0].settings, request.message.text)
#     url = "https://bot.jivosite.com/webhooks/QP8tRU0xZRjfXJm/4d383e39-5508-4d64-a938-f42daf546616"
#     json = response.dict()
#     headers  = {"Content-Type": "application/json"}
#     requests.post(url=url,headers=headers ,json=json)
#     return response.json()


# # @a_router.get("/assistant/all/{user_id}}",response_model=list[schemas.Assistant],name="Все ассистенты",description="Список ассистентов пользователя",tags=["Ассистент"])
# # async def create_user(user_id:int, db: Session = Depends(get_db)):
# #     result = db.get_user_assistant(user_id)
# #     if not result:
# #         return {"Message": "No one assistant added"}
# #     return result


# @a_router.post("/asistant/new/{access_token}",response_model=schemas.Assistant,name="Новый ассистент", description="Создание нового ассистента", tags=["Ассистент"])
# async def create_user(token:str, assistant: schemas.AssistantEntry, db: Session = Depends(get_db)):
#     user = crud.verify_token(db,token)
#     print(user.user_id)
#     new = schemas.Assistant(**assistant.dict(),user_id=user.user_id)
#     return crud.create_user_assistant(db=db, assistant=new)
