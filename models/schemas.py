from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4


class AssistantEntry(BaseModel):
    name: str
    settings: str = ""
    comment: str = None


class TgBotEntry(BaseModel):
    projectId: str
    botToken: str
    assistantId: str
    startMessage: str


class TgBotMessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str


class TgBotMessageChat(BaseModel):
    id: int
    first_name: str
    username: str
    type: str


class TgBotMessage(BaseModel):
    message_id: int
    from_: TgBotMessageFrom
    chat: TgBotMessageChat
    date: int
    text: str


class TgBotMessageEntry(BaseModel):
    update_id: int
    message: TgBotMessage


class TgUserBotEntry(BaseModel):
    api_id: str
    api_hash: str
    phone: str
    assistantId: str


class InstEntry(BaseModel):
    phone: str
    IdInstance: str
    ApiTokenInstance: str
    assistantId: str


class WaBotEntry(BaseModel):
    IdInstance: str
    ApiTokenInstance: str
    phone: str
    assistantId: str


class Message(BaseModel):

    type: str = "TEXT"
    text: str = None
    timestamp: int = datetime.timestamp(datetime.now())


class Channel(BaseModel):

    id: str = None
    type: str | None = None


class Sender(BaseModel):

    id: int | None = None
    user_token: str | None = None
    name: str | None = None
    url: str | None = None
    has_contacts: bool | None = None


class ClientMessage(BaseModel):

    id: str = None
    site_id: str = None
    client_id: str = None
    chat_id: str = None
    agents_online: bool = None
    sender: Sender
    message: Message
    channel: Channel
    event: str = "CLIENT_MESSAGE"


class JivoBotEntry(BaseModel):
    projectId: str
    assistantId: str
    provider_id: str


class BotMessage(BaseModel):
    id: str = None
    client_id: str = None
    chat_id: str = None
    message: Message = None
    event: str = "BOT_MESSAGE"


class Assistant(BaseModel):

    user_id: str = ""
    name: str = ""
    settings: str = ""
    use_count: str = 0
    comment: str = ""

    class Config:
        from_attributes = True


class ProfileEntry(BaseModel):
    name: str
    imageUrl: str = Field(None)
    email: str = None


class EditProfileEntry(BaseModel):
    name: str = None
    phone: str = None
    imageUrl: str = None
    telegram: str = None
    email: str = None
    company_name: str = None
    job_title: str = None


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
        from_attributes = True


class MessageRequest(BaseModel):

    user_id: str | None = None
    message: str | None = None


class MessageResponse(MessageRequest):

    user_id: str | None = None
    message: str | None = None
    answer: str | None = None
