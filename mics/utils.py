from fastapi import APIRouter, Path, Query, Request, HTTPException
from datetime import datetime
from prisma_ import prisma
from prisma import models


class Utils:

    @staticmethod
    async def check_expires(profile: models.Profile):

        is_pay = profile.expires >= datetime.now()
        if not is_pay:
            raise HTTPException(
                status_code=402, detail="Your access token is expired. Contact with us https://mind-market.ru/pay to pay for access")

        return True

    async def check_profile_access_token(self, access_token: str, checking_expires: bool = True):
        """ 
        Chect existing profile and check payment expires 

        Args:
            access_token (str): Profile token  
        Raises:
            HTTPException: status_code: 401 Your access token is not exist."
        """
        profile = await prisma.profile.find_first(
            where={"token": access_token},
            include={
                "assistants": True,
                "telegramBots": True,
                "telegramUserBots": True,
                "whatsAppBot": True

            }
        )

        if not profile:
            raise HTTPException(
                status_code=401, detail="Your access token is not exist.")
        if checking_expires:
            self.check_expires(profile=profile)
        return profile

    async def check_assistant_access_token(self, access_token: str):
        """ 
        Chect existing assistant token

        Args:
            access_token (str): Assistant token  
        Raises:
            HTTPException: status_code: 401 Your access token is not exist."
        """
        profile = await prisma.assistant.find_first(
            where={"token": access_token},
            include={
                "telegramBots": True,
                "telegramUserBots": True,
                "whatsAppBot": True,
                'jivoBot': True
            }
        )

        if not profile:
            raise HTTPException(
                status_code=401, detail="Your access token is not exist.")
        return profile
