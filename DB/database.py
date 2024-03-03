import dotenv
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
if not database_exists(engine.url):
    create_database(engine.url)


class Account(Base):
    __tablename__ = 'Account'

    id = Column(String(255), primary_key=True, default="cuid()")
    userId = Column(String(255), ForeignKey('User.id'), unique=True)
    providerType = Column(String(255), unique=True)
    providerId = Column(String(255), unique=True)
    providerAccountId = Column(String(255), unique=True)
    refreshToken = Column(String(255), unique=True)
    accessToken = Column(String(255), unique=True)
    accessTokenExpires = Column(DateTime)
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")
    User = relationship("User", back_populates="Account")


class Session(Base):
    __tablename__ = 'Session'

    id = Column(String(255), primary_key=True, default="cuid()")
    userId = Column(String(255), ForeignKey('User.id'), unique=True)
    expires = Column(DateTime)
    sessionToken = Column(String(255), unique=True)
    accessToken = Column(String(255), unique=True)
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")
    User = relationship("User", back_populates="Session")


class VerificationRequest(Base):
    __tablename__ = 'VerificationRequest'

    id = Column(String(255), primary_key=True, default="cuid()")
    identifier = Column(String(255))
    token = Column(String(255), unique=True)
    expires = Column(DateTime)
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class User(Base):
    __tablename__ = 'User'

    id = Column(String(255), primary_key=True, default="cuid()")
    name = Column(String(255))
    email = Column(String(255), unique=True)
    emailVerified = Column(DateTime)
    image = Column(String(255))
    userId = Column(String(255), unique=True)
    imageUrl = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default="uuid()")
    apiKey = Column(String(255), default="uuid()")
    job_title = Column(String(255))
    companyName = Column(String(255))
    phone_number = Column(String(255))
    telegram = Column(String(255))
    subscription_end = Column(DateTime)
    expires = Column(DateTime)
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")

    Project = relationship("Project", back_populates="owner")
    # ManagedProjects = relationship("Project", back_populates="Manager")
    Account = relationship("Account", back_populates="User")
    Session = relationship("Session", back_populates="User")

    # telegram_bots = relationship("TelegramBot", back_populates="user")
    # telegram_user_bots = relationship("TelegramUserBot", back_populates="user")
    # whatsapp_bots = relationship("WhatsAppBot", back_populates="user")
    # jivo_bots = relationship("JivoBot", back_populates="user")
    # Message = relationship("Message", back_populates="user")


class Project(Base):
    __tablename__ = 'Project'

    id = Column(String(255), primary_key=True, default="uuid()")
    name = Column(String(255))
    ownerId = Column(String(255), ForeignKey('User.id'))
    owner = relationship("User", back_populates="Project")

    Manager = relationship("Manager", back_populates="Project")

    Assistant = relationship("Assistant", back_populates="Project")
    Integration = relationship("Integration", back_populates="Project")
    Chats = relationship("Chat", back_populates="Project")
    Client = relationship("Client", back_populates="Project")

    Quiz = relationship("Quiz", back_populates="Project")
    Deals = relationship("Deal", back_populates="Project")
    Tasks = relationship("Task", back_populates="Project")
    WhatsAppBot = relationship("WhatsAppBot", back_populates="Project")
    TelegramUserBot = relationship(
        "TelegramUserBot", back_populates="Project")
    TelegramBot = relationship("TelegramBot", back_populates="Project")
    JivoBot = relationship("JivoBot", back_populates="Project")

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class Assistant(Base):
    __tablename__ = 'Assistant'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Assistant")

    name = Column(String(255))
    comment = Column(String(255))
    settings = Column(String(255))
    image_url = Column(String(255))
    use_count = Column(Integer, default=0)
    access_token = Column(String(255), default="uuid()")

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")

    Integration = relationship("Integration", back_populates="Assistant")
    Chat = relationship("Chat", back_populates="Assistant")

    # telegram_bots = relationship("TelegramBot", back_populates="assistant")
    # telegram_user_bots = relationship(
    #     "TelegramUserBot", back_populates="assistant")
    # whatsapp_bots = relationship("WhatsAppBot", back_populates="assistant")
    # jivo_bots = relationship("JivoBot", back_populates="assistant")
    # Message = relationship("Message", back_populates="assistant")


class Integration(Base):
    __tablename__ = 'Integration'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Integration")

    service_type = Column(String(255))
    service_id = Column(String(255))
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))

    Assistant = relationship("Assistant", back_populates="Integration")
    Chats = relationship("Chat", back_populates="Integration")
    # Manager = relationship("Manager", back_populates="Integration")


class Chat(Base):
    __tablename__ = 'Chat'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Chats")

    managerId = Column(String(255))
    client_id = Column(String(255), unique=True)
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    managerId = Column(String(255), ForeignKey('Manager.id'))
    integrationId = Column(String(255), ForeignKey('Integration.id'))
    is_blocked = Column(Boolean, default=False)
    is_assistant_in_chat = Column(Boolean, default=True)
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")

    Manager = relationship("Manager", back_populates="Chat")
    client = relationship("Client", back_populates="Chat")
    Assistant = relationship("Assistant", back_populates="Chat")
    Integration = relationship("Integration", back_populates="Chats")
    Messages = relationship("Message", back_populates="Chat")


class Client(Base):
    __tablename__ = 'Client'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Client")

    chatId = Column(String(255), ForeignKey('Chat.id'))
    name = Column(String(255))
    username = Column(String(255))
    image_url = Column(String(255))
    category = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    about = Column(String(255))
    companyName = Column(String(255))
    tags = Column(String(255))
    in_service_id = Column(String(255))

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")

    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Client")
    Chat = relationship("Chat", back_populates="client")


class Manager(Base):
    __tablename__ = 'Manager'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Manager")

    integration_id = Column(String(255), ForeignKey('Integration.id'))
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")
    # userId = relationship("Project", back_populates="Manager")
    Tasks = relationship("Task", back_populates="Manager")
    Deals = relationship("Deal", back_populates="Manager")
    Client = relationship("Client", back_populates="Manager")
    Chat = relationship("Chat", back_populates="Manager")
    Messages = relationship("Message", back_populates="Manager")
    # integration = relationship("Integration", back_populates="Manager")


class Message(Base):
    __tablename__ = 'Message'

    id = Column(String(255), primary_key=True, default="uuid()")
    chat_id = Column(String(255), ForeignKey('Chat.id'))
    text = Column(String(255))
    files_url = Column(String(255))
    images_url = Column(String(255))
    incoming = Column(Boolean, default=True)
    from_assistant = Column(Boolean, default=False)
    from_user = Column(Boolean, default=False)
    from_manager = Column(Boolean, default=False)
    managerId = Column(String(255), ForeignKey("Manager.id"))
    assistant_id = Column(String(255))
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default="now()")
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")

    # projectId = Column(String(255), ForeignKey('Project.id'))
    # Project = relationship("Project", back_populates="Assistant")
    Chat = relationship("Chat", back_populates="Messages")
    Manager = relationship("Manager", back_populates="Messages")
    # assistant = relationship("Assistant", back_populates="Messages")


class JivoBot(Base):
    __tablename__ = 'JivoBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="JivoBot")

    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class TelegramBot(Base):
    __tablename__ = 'TelegramBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="TelegramBot")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class TelegramUserBot(Base):
    __tablename__ = 'TelegramUserBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="TelegramUserBot")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class WhatsAppBot(Base):
    __tablename__ = 'WhatsAppBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="WhatsAppBot")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")


class Task(Base):
    __tablename__ = 'Task'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Tasks")
    stage = Column(String(255))
    text = Column(String(255))
    clientId = Column(String(255))
    createdAt = Column(DateTime, default="now()")
    updatedAt = Column(DateTime, onupdate="now()")
    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Tasks")


class Quiz(Base):
    __tablename__ = 'Quiz'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Quiz")


class Deal(Base):
    __tablename__ = 'Deal'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Deals")
    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Deals")


Base.metadata.create_all(engine)
