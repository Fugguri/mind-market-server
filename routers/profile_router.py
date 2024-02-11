from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from DB import db


profile_router = APIRouter()


@profile_router.get("/profile/{id}", name="Данные профиля", description="Данные о пользователе", tags=["Профиль"])
async def profile(id: str | int):
    db.get_user(id)
    return profile


@profile_router.patch("/profile/{id}", name="Обновить данные профиль", description="Обновление данных профиля", tags=["Профиль"])
async def profile(id:  str | int):
    db.get_user(id)
    return profile


@profile_router.delete("/profile/{id}", name="Удалить профиль", description="Удаление профиля по id", tags=["Профиль"])
async def profile(id:  str | int):
    db.get_user(id)
    return profile


@profile_router.post("/profile/new", name="Новый пользователь", tags=["Профиль"])
async def create_profile(profile: schemas.ProfileEntry):
    ...
