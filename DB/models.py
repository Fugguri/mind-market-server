import datetime
from uuid import uuid4
from .db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = 'Account'

    id = Column(String(255), primary_key=True, default=uuid4())
    userId = Column(String(255), ForeignKey('User.id'), unique=True)
    providerType = Column(String(255), unique=True)
    providerId = Column(String(255), unique=True)
    providerAccountId = Column(String(255), unique=True)
    refreshToken = Column(String(255), unique=True)
    accessToken = Column(String(255), unique=True)
    accessTokenExpires = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())
    User = relationship("User", back_populates="Account", lazy="selectin")


class Session(Base):
    __tablename__ = 'Session'

    id = Column(String(255), primary_key=True, default=uuid4())
    userId = Column(String(255), ForeignKey('User.id'), unique=True)
    expires = Column(DateTime)
    sessionToken = Column(String(255), unique=True)
    accessToken = Column(String(255), unique=True)
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())
    User = relationship("User", back_populates="Session", lazy="selectin")


class VerificationRequest(Base):
    __tablename__ = 'VerificationRequest'

    id = Column(String(255), primary_key=True, default=uuid4())
    identifier = Column(String(255))
    token = Column(String(255), unique=True)
    expires = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class User(Base):
    __tablename__ = 'User'

    id = Column(String(255), primary_key=True, default=uuid4())
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
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())

    Project = relationship("Project", back_populates="owner", lazy="selectin")
    # ManagedProjects = relationship("Project", back_populates="Manager",lazy="selectin")
    Account = relationship("Account", back_populates="User", lazy="selectin")
    Session = relationship("Session", back_populates="User", lazy="selectin")

    # telegram_bots = relationship("TelegramBot", back_populates="user",lazy="selectin")
    # telegram_user_bots = relationship("TelegramUserBot", back_populates="user",lazy="selectin")
    # whatsapp_bots = relationship("WhatsAppBot", back_populates="user",lazy="selectin")
    # jivo_bots = relationship("JivoBot", back_populates="user",lazy="selectin")
    # Message = relationship("Message", back_populates="user",lazy="selectin")


class Project(Base):
    __tablename__ = 'Project'

    id = Column(String(255), primary_key=True, default="uuid()")
    name = Column(String(255))
    ownerId = Column(String(255), ForeignKey('User.id'))
    owner = relationship("User", back_populates="Project", lazy="selectin")

    Manager = relationship(
        "Manager", back_populates="Project", lazy="selectin")

    Assistant = relationship(
        "Assistant", back_populates="Project", lazy="selectin")
    Integration = relationship(
        "Integration", back_populates="Project", lazy="selectin")
    Chats = relationship("Chat", back_populates="Project", lazy="selectin")
    Client = relationship("Client", back_populates="Project", lazy="selectin")

    Quiz = relationship("Quiz", back_populates="Project", lazy="selectin")
    Deals = relationship("Deal", back_populates="Project", lazy="selectin")
    Tasks = relationship("Task", back_populates="Project", lazy="selectin")
    WhatsAppBot = relationship(
        "WhatsAppBot", back_populates="Project", lazy="selectin")
    TelegramUserBot = relationship(
        "TelegramUserBot", back_populates="Project", lazy="selectin")
    TelegramBot = relationship(
        "TelegramBot", back_populates="Project", lazy="selectin")
    JivoBot = relationship(
        "JivoBot", back_populates="Project", lazy="selectin")

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class Assistant(Base):
    __tablename__ = 'Assistant'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="Assistant", lazy="selectin")

    name = Column(String(255))
    comment = Column(String(255))
    settings = Column(String(255))
    imageUrl = Column(String(255))
    use_count = Column(Integer, default=0)
    access_token = Column(String(255), default="uuid()")

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())

    Integration = relationship(
        "Integration", back_populates="Assistant", lazy="selectin")
    Chat = relationship("Chat", back_populates="Assistant", lazy="selectin")

    # telegram_bots = relationship("TelegramBot", back_populates="assistant",lazy="selectin")
    # telegram_user_bots = relationship,lazy="selectin")(
    #     "TelegramUserBot", back_populates="assistant")
    # whatsapp_bots = relationship("WhatsAppBot", back_populates="assistant",lazy="selectin")
    # jivo_bots = relationship("JivoBot", back_populates="assistant",lazy="selectin")
    # Message = relationship("Message", back_populates="assistant",lazy="selectin")


class Integration(Base):
    __tablename__ = 'Integration'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="Integration", lazy="selectin")

    service_type = Column(String(255))
    service_id = Column(String(255))
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))

    Assistant = relationship(
        "Assistant", back_populates="Integration", lazy="selectin")
    Chats = relationship("Chat", back_populates="Integration", lazy="selectin")
    # Manager = relationship("Manager", back_populates="Integration",lazy="selectin")


class Chat(Base):
    __tablename__ = 'Chat'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Chats", lazy="selectin")

    managerId = Column(String(255))
    client_id = Column(String(255), unique=True)
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    managerId = Column(String(255), ForeignKey('Manager.id'))
    integrationId = Column(String(255), ForeignKey('Integration.id'))
    is_blocked = Column(Boolean, default=False)
    is_assistant_in_chat = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())

    Manager = relationship("Manager", back_populates="Chat", lazy="selectin")
    client = relationship("Client", back_populates="Chat", lazy="selectin")
    Assistant = relationship(
        "Assistant", back_populates="Chat", lazy="selectin")
    Integration = relationship(
        "Integration", back_populates="Chats", lazy="selectin")
    Messages = relationship("Message", back_populates="Chat", lazy="selectin")


class Client(Base):
    __tablename__ = 'Client'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Client", lazy="selectin")

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

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())

    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Client", lazy="selectin")
    Chat = relationship("Chat", back_populates="client", lazy="selectin")


class Manager(Base):
    __tablename__ = 'Manager'

    id = Column(String(255), primary_key=True, default="uuid()")
    ProjectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="Manager", lazy="selectin")

    integration_id = Column(String(255), ForeignKey('Integration.id'))
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())
    # userId = relationship("Project", back_populates="Manager",lazy="selectin")
    Tasks = relationship("Task", back_populates="Manager", lazy="selectin")
    Deals = relationship("Deal", back_populates="Manager", lazy="selectin")
    Client = relationship("Client", back_populates="Manager", lazy="selectin")
    Chat = relationship("Chat", back_populates="Manager", lazy="selectin")
    Messages = relationship(
        "Message", back_populates="Manager", lazy="selectin")
    # integration = relationship("Integration", back_populates="Manager",lazy="selectin")


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
    timestamp = Column(DateTime, default=datetime.datetime.now())
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())

    # projectId = Column(String(255), ForeignKey('Project.id'))
    # Project = relationship("Project", back_populates="Assistant",lazy="selectin")
    Chat = relationship("Chat", back_populates="Messages", lazy="selectin")
    Manager = relationship(
        "Manager", back_populates="Messages", lazy="selectin")
    # assistant = relationship("Assistant", back_populates="Messages",lazy="selectin")


class JivoBot(Base):
    __tablename__ = 'JivoBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="JivoBot", lazy="selectin")

    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class TelegramBot(Base):
    __tablename__ = 'TelegramBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    telegram_id = Column(BigInteger)
    botToken = (String(255))
    is_bot = Column(Boolean, default=True)
    first_name = Column(String(255))
    username = Column(String(255))
    can_join_groups = Column(Boolean, default=True)
    can_read_all_group_messages = Column(Boolean, default=False)
    supports_inline_queries = Column(Boolean, default=False)
    startMessage = Column(Text)

    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="TelegramBot", lazy="selectin")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class TelegramUserBot(Base):
    __tablename__ = 'TelegramUserBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="TelegramUserBot", lazy="selectin")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class WhatsAppBot(Base):
    __tablename__ = 'WhatsAppBot'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship(
        "Project", back_populates="WhatsAppBot", lazy="selectin")
    assistant_id = Column(String(255), ForeignKey('Assistant.id'))
    provider_id = Column(String(255))

    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())


class Task(Base):
    __tablename__ = 'Task'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Tasks", lazy="selectin")
    stage = Column(String(255))
    text = Column(String(255))
    clientId = Column(String(255))
    createdAt = Column(DateTime, default=datetime.datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.datetime.now())
    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Tasks", lazy="selectin")


class Quiz(Base):
    __tablename__ = 'Quiz'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Quiz", lazy="selectin")


class Deal(Base):
    __tablename__ = 'Deal'

    id = Column(String(255), primary_key=True, default="uuid()")
    projectId = Column(String(255), ForeignKey('Project.id'))
    Project = relationship("Project", back_populates="Deals", lazy="selectin")
    managerId = Column(String(255), ForeignKey('Manager.id'))
    Manager = relationship("Manager", back_populates="Deals", lazy="selectin")
