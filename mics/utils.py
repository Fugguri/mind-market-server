from fastapi import APIRouter, Path, Query, Request, HTTPException
from datetime import datetime
from prisma_ import prisma
from prisma import models


class Utils:

    @staticmethod
    async def check_expires(user: models.User):

        is_pay = user.expires <= datetime.now()
        if not is_pay:
            raise HTTPException(
                status_code=402, detail="Your access token is expired. Contact with us https://mind-market.ru/pay to pay for access")

        return True

    async def check_user_access_token(self, access_token: str, checking_expires: bool = True):
        """ 
        Chect existing user and check payment expires 

        Args:
            access_token (str): user token  
        Raises:
            HTTPException: status_code: 401 Your access token is not exist."
        """
        user = await prisma.user.find_first(
            where={"token": access_token},
            include={
                "assistants": True,
                "telegramBots": True,
                "telegramUserBots": True,
                "whatsAppBot": True

            }
        )

        if not user:
            raise HTTPException(
                status_code=401, detail="Your access token is not exist.")
        if checking_expires:
            self.check_expires(user=user)
        return user

    async def check_assistant_access_token(self, access_token: str):
        """ 
        Chect existing assistant token

        Args:
            access_token (str): Assistant token  
        Raises:
            HTTPException: status_code: 401 Your access token is not exist."
        """
        print(access_token)

        assistant = await prisma.assistant.find_first(
            where={"token": access_token},
            include={
                "telegramBots": True,
                "telegramUserBots": True,
                "whatsAppBot": True,
                'jivoBot': True,
                "user": True
            }
        )
        if not assistant:
            raise HTTPException(
                status_code=401, detail="Your access token is not exist.")
        if assistant.name == "Сергей":
            raise HTTPException(
                status_code=402, detail="Your access token is expired. Contact help to pay for access")

        return assistant
