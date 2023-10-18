from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4


class AssistantEntry(BaseModel):
    name: str
    settings: str = ""
    comment: str = None


class Sender(BaseModel):

    id: int | None = None
    user_token: str | None = None
    name: str | None = None
    url: str | None = None
    has_contacts: bool | None = None


class TgBotEntry(BaseModel):
    token: str


class TgUserBotEntry(BaseModel):
    api_id: str
    api_hash: str
    phone: str


class InstEntry(BaseModel):
    phone: str
    IdInstance: str
    ApiTokenInstance: str


class WaBotEntry(BaseModel):
    IdInstance: str
    ApiTokenInstance: str
    phone: str


class Message(BaseModel):

    type: str = "TEXT"
    text: str = None
    timestamp: float = datetime.timestamp(datetime.now())


class Channel(BaseModel):

    id: str = None
    type: str | None = None


class ClientMessage(BaseModel):

    id: str = None
    site_id: str = None
    client_id: str = None
    chat_id: str = None
    agents_online: bool = None
    sender: Sender | None = None
    message: Message = None
    channel: Channel = None
    event: str = None


class BotMessage(BaseModel):
    id: str = None
    event: str = "BOT_MESSAGE"
    client_id: str = None
    chat_id: str = None
    message: Message = None


class Assistant(BaseModel):

    user_id: str = ""
    name: str = ""
    settings: str = ""
    use_count: str = 0
    comment: str = ""

    class Config:
        orm_mode = True


class ProfileEntry(BaseModel):
    name: str
    imageUrl: str = Field(None)
    email: str = None


class User(BaseModel):

    user_id: int | str = str(uuid4())
    username: str | int
    password: str | int      # todo! password validation func
    full_name: str | None = None
    company_name: str | None = None
    token: str = str(uuid4())
    expires: datetime = datetime.now() + timedelta(days=3)
    assistants: list[Assistant] = []
    provider_id: str | None = None

    class Config:
        orm_mode = True


class MessageRequest(BaseModel):

    user_id: str | None = None
    message: str | None = None


class MessageResponse(MessageRequest):

    user_id: str | None = None
    message: str | None = None
    answer: str | None = None
