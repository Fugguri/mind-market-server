from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import dotenv

DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default="cuid()")
    name = Column(String)
    email = Column(String, unique=True)
    email_verified = Column(DateTime)
    image = Column(String)
    user_id = Column(String, unique=True)
    image_url = Column(String)
    login = Column(String)
    password = Column(String)
    token = Column(String, default="uuid()")
    expires_in = Column(DateTime)
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    assistants = relationship("Assistant", back_populates="user")
    integrations = relationship("Integration", back_populates="user")
    chats = relationship("Chat", back_populates="user")
    clients = relationship("Client", back_populates="user")
    owned_managers = relationship(
        "Manager", back_populates="owner", foreign_keys="[Manager.owner_id]")
    managed_by = relationship(
        "Manager", back_populates="manager", foreign_keys="[Manager.managed_by_id]")
    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    quizzes = relationship("Quiz", back_populates="user")
    telegram_bots = relationship("TelegramBot", back_populates="user")
    telegram_user_bots = relationship("TelegramUserBot", back_populates="user")
    whatsapp_bots = relationship("WhatsAppBot", back_populates="user")
    jivo_bots = relationship("JivoBot", back_populates="user")
    messages = relationship("Message", back_populates="user")


class Assistant(Base):
    __tablename__ = 'assistants'

    id = Column(String, primary_key=True, default="uuid()")
    user_id = Column(String, ForeignKey('users.id'))
    name = Column(String)
    comment = Column(String)
    settings = Column(String)
    image_url = Column(String)
    use_count = Column(Integer, default=0)
    access_token = Column(String, default="uuid()")
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    user = relationship("User", back_populates="assistants")
    integrations = relationship("Integration", back_populates="assistant")
    chats = relationship("Chat", back_populates="assistant")
    telegram_bots = relationship("TelegramBot", back_populates="assistant")
    telegram_user_bots = relationship(
        "TelegramUserBot", back_populates="assistant")
    whatsapp_bots = relationship("WhatsAppBot", back_populates="assistant")
    jivo_bots = relationship("JivoBot", back_populates="assistant")
    messages = relationship("Message", back_populates="assistant")


class Integration(Base):
    __tablename__ = 'integrations'

    id = Column(String, primary_key=True, default="uuid()")
    user_id = Column(String, ForeignKey('users.id'))
    service_type = Column(String)
    service_id = Column(String)
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")
    assistant_id = Column(String, ForeignKey('assistants.id'))

    user = relationship("User", back_populates="integrations")
    assistant = relationship("Assistant", back_populates="integrations")
    chats = relationship("Chat", back_populates="integration")
    managers = relationship("Manager", back_populates="integration")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(String, primary_key=True, default="uuid()")
    user_id = Column(String, ForeignKey('users.id'))
    manager_id = Column(String)
    client_id = Column(String, unique=True)
    assistant_id = Column(String)
    integration_id = Column(String)
    is_blocked = Column(Boolean, default=False)
    is_assistant_in_chat = Column(Boolean, default=True)
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    user = relationship("User", back_populates="chats")
    manager = relationship("Manager", back_populates="chats")
    client = relationship("Client", back_populates="chats")
    assistant = relationship("Assistant", back_populates="chats")
    integration = relationship("Integration", back_populates="chats")
    messages = relationship("Message", back_populates="chat")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True, default="uuid()")
    user_id = Column(String, ForeignKey('users.id'))
    manager_id = Column(String, ForeignKey('managers.id'))
    chat_id = Column(String)
    name = Column(String)
    username = Column(String)
    image_url = Column(String)
    category = Column(String)
    email = Column(String)
    phone = Column(String)
    about = Column(String)
    company_name = Column(String)
    tags = Column(String)
    in_service_id = Column(String)
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    user = relationship("User", back_populates="clients")
    manager = relationship("Manager", back_populates="clients")
    chats = relationship("Chat", back_populates="client")


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(String, primary_key=True, default="uuid()")
    owner_id = Column(String, ForeignKey('users.id'))
    manager_id = Column(String)
    managed_by_id = Column(String, ForeignKey('users.id'))
    integration_id = Column(String, ForeignKey('integrations.id'))
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    owner = relationship("User", back_populates="owned_managers")
    manager = relationship("User", back_populates="managed_by")
    tasks = relationship("Task", back_populates="manager")
    deals = relationship("Deal", back_populates="manager")
    clients = relationship("Client", back_populates="manager")
    chats = relationship("Chat", back_populates="manager")
    messages = relationship("Message", back_populates="manager")
    integration = relationship("Integration", back_populates="managers")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default="uuid()")
    chat_id = Column(String, ForeignKey('chats.id'))
    text = Column(String)
    files_url = Column(String)
    images_url = Column(String)
    incoming = Column(Boolean, default=True)
    from_assistant = Column(Boolean, default=False)
    from_user = Column(Boolean, default=False)
    from_manager = Column(Boolean, default=False)
    manager_id = Column(String)
    user_id = Column(String)
    assistant_id = Column(String)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default="now()")
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    chat = relationship("Chat", back_populates="messages")
    manager = relationship("Manager", back_populates="messages")
    user = relationship("User", back_populates="messages")
    assistant = relationship("Assistant", back_populates="messages")


Base.metadata.create_all(engine)
