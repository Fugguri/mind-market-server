from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from prisma_ import prisma
from prisma import models
from mics import utls


webhooks_router = APIRouter()


@webhooks_router.get("/webhook/tg_bot/{access_token}", response_model=models.Profile, name="Данные профиля", description="Данные по пользователе", tags=["Профиль"])
async def profile(access_token: str):
    profile = await utls.check_profile_access_token(access_token, False)
    print(profile)
    return profile
