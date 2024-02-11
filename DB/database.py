from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import dotenv

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Account(Base):
    __tablename__ = 'Account'

    id = Column(String(255), primary_key=True, default='cuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    providerType = Column(String(255))
    providerId = Column(String(255))
    providerAccountId = Column(String(255))
    refreshToken = Column(String(255))
    accessToken = Column(String(255))
    accessTokenExpires = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow)
    user = relationship("User", back_populates="accounts")

    __table_args__ = (
        UniqueConstraint('providerId', 'providerAccountId',
                         name='_provider_unique_constraint'),
    )


class Session(Base):
    __tablename__ = 'Session'

    id = Column(String(255), primary_key=True, default='cuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    expires = Column(DateTime)
    sessionToken = Column(String(255), unique=True)
    accessToken = Column(String(255), unique=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow)
    user = relationship("User", back_populates="sessions")


class User(Base):
    __tablename__ = 'User'

    id = Column(String(255), primary_key=True, default='cuid()')
    name = Column(String(255))
    email = Column(String(255), unique=True)
    emailVerified = Column(DateTime)
    image = Column(String(255))
    userId = Column(String(255), unique=True)
    imageUrl = Column(Text)
    login = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default='uuid()')

    assistants = relationship("Assistant", back_populates="user")
    integrations = relationship("Integrations", back_populates="user")
    chats = relationship("Chat", back_populates="user")
    clients = relationship("Client", back_populates="user")
    managers = relationship("Manager", back_populates="user")

    expires = Column(
        DateTime, default=datetime.datetime.utcnow() + datetime.timedelta(days=3))

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow)


class VerificationRequest(Base):
    __tablename__ = 'VerificationRequest'

    id = Column(String(255), primary_key=True, default='cuid()')
    identifier = Column(String(255))
    token = Column(String(255), unique=True)
    expires = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('identifier', 'token',
                         name='_identifier_token_unique_constraint'),
    )


class Quiz(Base):
    __tablename__ = 'Quiz'
    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    companyName = Column(Text)
    companyCategory = Column(Text)
    aiGoals = Column(Text)
    aiRole = Column(Text)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Task(Base):
    __tablename__ = 'Task'
    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    managerId = Column(String(255), ForeignKey('Manager.id'))
    stage = Column(Text)
    text = Column(Text)

    clientId = Column(String(255), ForeignKey('Client.id'))

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Deal(Base):
    __tablename__ = 'Deal'
    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    managerId = Column(String(255), ForeignKey('Manager.id'))
    amount = Column(Integer)
    stage = Column(Text)
    text = Column(Text)

    clientId = Column(String(255), ForeignKey('Client.id'))

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Assistant(Base):
    __tablename__ = 'Assistant'

    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    name = Column(String(255))
    comment = Column(Text)
    settings = Column(Text)
    imageUrl = Column(Text)
    use_count = Column(Integer, default=0)
    access_token = Column(String(255), default='uuid()')
    user = relationship("User", back_populates="assistants")
    integrations = relationship("Integration", back_populates="assistant")
    chats = relationship("Chat", back_populates="assistant")

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class TelegramBot(Base):
    __tablename__ = 'TelegramBot'

    id = Column(String(255), primary_key=True, default='uuid()')
    name = Column(Text)
    telegram_id = Column(Text)
    imageUrl = Column(Text)
    useCount = Column(Integer, default=0)
    token = Column(Text)
    userId = Column(String(255), ForeignKey('User.id'))
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="telegramBots")
    user = relationship("User", back_populates="telegramBots")


class TelegramUserBot(Base):
    __tablename__ = 'TelegramUserBot'

    id = Column(String(255), primary_key=True, default='uuid()')
    firstName = Column(Text)
    lastName = Column(Text)
    username = Column(Text)
    imageUrl = Column(Text)
    useCount = Column(Integer, default=0)
    phone = Column(Text)
    api_id = Column(Text)
    api_hash = Column(Text)
    userId = Column(String(255), ForeignKey('User.id'))
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="telegramUserBots")
    user = relationship("User", back_populates="telegramUserBots")


class WhatsAppBot(Base):
    __tablename__ = 'WhatsAppBot'

    id = Column(String(255), primary_key=True, default='uuid()')
    name = Column(Text)
    settings = Column(Text)
    imageUrl = Column(Text)
    useCount = Column(Integer, default=0)
    fullName = Column(Text)
    phone = Column(Text)
    IdInstance = Column(Text)
    ApiTokenInstance = Column(Text)
    userId = Column(String(255), ForeignKey('User.id'))
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="whatsAppBot")
    user = relationship("User", back_populates="whatsAppBot")


class JivoBot(Base):
    __tablename__ = 'JivoBot'

    id = Column(String(255), primary_key=True, default='uuid()')
    name = Column(Text)
    settings = Column(Text)
    imageUrl = Column(Text)
    useCount = Column(Integer, default=0)
    provider_id = Column(Text)
    userId = Column(String(255), ForeignKey('User.id'))
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="jivoBot")
    user = relationship("User", back_populates="jivoBot")


class Client(Base):
    __tablename__ = 'Client'

    id = Column(String(255), primary_key=True, default='uuid()')

    userId = Column(String(255), ForeignKey('User.id'))
    user = relationship("User", back_populates="clients")
    managerId = Column(String(255), ForeignKey('Manager.id'))
    chatId = Column(String(255), ForeignKey('Manager.id'))
    chat = relationship("Chat", back_populates="client")
    manager = relationship("Manager", back_populates="clients")

    name = Column(Text)
    username = Column(Text)
    imageUrl = Column(Text)
    category = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    about = Column(Text)
    company_name = Column(Text)
    tags = Column(Text)

    InServiceId = Column(Text)

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Manager(Base):
    __tablename__ = 'Manager'

    id = Column(String(255), primary_key=True, default='uuid()')
    ownerId = Column(String(255), ForeignKey('User.id'))
    manager_id = Column(String(255), ForeignKey('User.id'))
    owner = relationship("User", back_populates="owner")
    manager = relationship("User", back_populates="manager")

    tasks = relationship("Task", back_populates="manager")
    deals = relationship("Deal", back_populates="manager")
    clients = relationship("Client", back_populates="manager")
    chats = relationship("Chat", back_populates="manager")
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Chat(Base):
    __tablename__ = 'Chat'

    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    user = relationship("User", back_populates="chats")
    managerId = Column(String(255), ForeignKey('Manager.id'))
    manager = relationship("Manager", back_populates="chats")
    clientId = Column(String(255), ForeignKey('Client.id'))
    client = relationship("Client", back_populates="chats")
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="chats")
    integrationId = Column(String(255), ForeignKey('Integration.id'))
    integration = relationship("Integration", back_populates="chats")

    isBlocked = Column(Boolean, default=False)
    isAssistantInChat = Column(Boolean, default=True)

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class Message(Base):
    __tablename__ = 'Message'

    id = Column(String(255), primary_key=True, default='uuid()')
    chatId = Column(String(255), ForeignKey('Chat.id'))
    chat = relationship("Chat", back_populates="messages")

    text = Column(Text)
    filesUrl = Column(Text)
    imagesUrl = Column(Text)

    incoming = Column(Boolean, default=True)

    fromAssistant = Column(Boolean, default=False)
    fromUser = Column(Boolean, default=False)
    fromManager = Column(Boolean, default=False)

    managerId = Column(String(255), ForeignKey('Manager.id'))
    manager = relationship("Manager", back_populates="messages")
    userId = Column(String(255), ForeignKey('User.id'))
    user = relationship("User", back_populates="messages")
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="messages")

    isRead = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


class integration(Base):
    __tablename__ = 'Integration'

    id = Column(String(255), primary_key=True, default='uuid()')
    userId = Column(String(255), ForeignKey('User.id'))
    user = relationship("User", back_populates="integration")

    serviceType = Column(String(255))
    serviceId = Column(String(255))

    chats = relationship("Chat", back_populates="integration")
    managers = relationship("Manager", back_populates="integration")
    assistantId = Column(String(255), ForeignKey('Assistant.id'))
    assistant = relationship("Assistant", back_populates="integration")

    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.datetime.utcnow())


Base.metadata.create_all(engine)
