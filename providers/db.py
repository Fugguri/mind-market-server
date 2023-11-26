from prisma import models
from prisma_ import prisma


async def create_client(name, username, InChannelId: str, userId):

    return await prisma.client.create(data={
        "name": name,
        "username": username,
        "InChannelId": InChannelId,
        "userId": userId
    })


async def create_chat(channelType: models.enums.ChannelType,
                      userId,
                      clientId,
                      assistantId=None,
                      operatorId=None):

    return await prisma.chat.create(data={
        "channelType": channelType,
        "userId": userId,
        "clientId": clientId,
        "assistantId": assistantId,
        "operatorId": operatorId
    })


async def create_message(content: models.enums.ChannelType,
                         chatId,
                         fileUrl=None,
                         fromClient=True,
                         operatorId=None):

    return await prisma.chat.create(data={
        "content": content,
        "chatId": chatId,
        "fileUrl": fileUrl,
        "fromClient": fromClient,
        "operatorId": operatorId
    })

# ---------------- getters


async def get_telegrambot(bot_id: str | int) -> models.TelegramBot:
    return await prisma.telegrambot.find_first(where={
        "id": bot_id
    }, include={
        "user": True,
        "assistant": True
    })


async def get_chat(user: models.User, client: models.Client) -> models.Chat:

    chat = await prisma.chat.find_unique(where={
        "userId"
    })

    return chat


async def get_client(InChannelId: str | int) -> models.Client:
    return await prisma.client.query_first('SELECT * FROM Client WHERE InChannelId = ?',
                                           InChannelId,
                                           )
