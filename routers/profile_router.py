from fastapi import APIRouter, Path, Query, Request, HTTPException
from models import schemas
from prisma_ import prisma
from prisma import models
from mics import utls


profile_router = APIRouter()


@profile_router.get("/profile/{access_token}", response_model=models.Profile, name="Данные профиля", description="Данные по пользователе", tags=["Профиль"])
async def profile(access_token: str):
    profile = await utls.check_profile_access_token(access_token, False)
    return profile


@profile_router.put("/profile/new", name="Редактировать профиль", tags=["Профиль"])
async def create_profile(profile: schemas.ProfileEntry):
    prisma.profile.create(data={
        "name": profile.name,
        "imageUrl": profile.imageUrl,
        "email": profile.email
    })


@profile_router.post("/profile/new", name="Новый пользователь", tags=["Профиль"])
async def create_profile(profile: schemas.ProfileEntry):
    prisma.profile.create(data={
        "name": profile.name,
        "imageUrl": profile.imageUrl,
        "email": profile.email,
    })


# @u_router.get("/profiles/" ,name="Все пользователи", tags=["Пользователь"])
# async def profiles(db: Session = Depends(get_db)):
#     db_profile = await crud.get_profiles(db)
#     if not db_profile:
#         raise HTTPException(status_code=400, detail="There is no profiles")
#     return {"profiles_list": db_profile}
