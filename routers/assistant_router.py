from fastapi import APIRouter, HTTPException
from models import schemas
from prisma import models
from prisma_ import prisma
from mics import utls
assistant_router = APIRouter()


@assistant_router.post("/api_v2/assistants/{access_token}/{assistant_id}", name="Использовать ассистента", description="Запрос ответа от ассистента", tags=["Ассистенты"])
async def create_user(access_token: str, assistant_id: str, ):
    profile = await utls.check_profile_access_token(access_token, False)
    for assistant in profile.assistants:
        if assistant_id == assistant.id:
            return assistant

    raise HTTPException(status_code=401, detail="Assistant is not exist.")


@assistant_router.get("/api_v2/assistants/{access_token}/{assistant_id}", name="Текущий ассистент", description="Запрос информации об ассистенте", tags=["Ассистенты"])
async def create_user(access_token: str, assistant_id: str, ):
    profile = await utls.check_profile_access_token(access_token, False)

    for assistant in profile.assistants:
        if assistant_id == assistant.id:
            return assistant

    raise HTTPException(status_code=401, detail="Assistant is not exist.")


@assistant_router.post("/api_v2/assistants/new/{access_token}", name="Новый ассистент", description="Создание ассистента", tags=["Ассистенты"])
async def create_user(access_token: str, assistant: schemas.AssistantEntry):
    profile = await utls.check_profile_access_token(access_token, False)

    new = prisma.assistant.create(
        data={
            "profileId": profile.id,
            "name": assistant.name,
            "settings": assistant.settings,
            "comment": assistant.comment
        }
    )

    return new


@assistant_router.post("/api_v2/assistants/edit/{access_token}", name="Редактировать ассистента", description="Редактирование ассистента ассистента", tags=["Ассистенты"])
async def create_user(access_token: str, assistant: schemas.AssistantEntry):
    profile = await utls.check_profile_access_token(access_token, False)

    new = prisma.assistant.update(
        data={
            "profileId": profile.id,
            "name": assistant.name,
            "settings": assistant.settings,
            "comment": assistant.comment
        },
        where={
            "name": assistant.name
        }
    )

    return new


@assistant_router.get("/assistants/all/{access_token}", response_model=list[schemas.Assistant], name="Все ассистенты", description="Список ассистентов пользователя", tags=["Ассистенты"])
async def create_user(access_token: str):
    profile = await utls.check_profile_access_token(access_token, False)

    if len(profile.assistants) == 0:
        raise HTTPException(status_code=401, detail="No one assistant added.")

    return profile.assistants
