from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy import UniqueConstraint, create_engine, Column, Integer, DateTime, Boolean, Text, ForeignKey, Enum
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

    id = Column(String(255), primary_key=True, default="cuid()")
    name = Column(String(255))
    email = Column(String(255), unique=True)
    email_verified = Column(DateTime)
    image = Column(String(255))
    user_id = Column(String(255), unique=True)
    image_url = Column(String(255))
    login = Column(String(255))
    password = Column(String(255))
    token = Column(String(255), default="uuid()")
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

    id = Column(String(255), primary_key=True, default="uuid()")
    user_id = Column(String(255), ForeignKey('users.id'))
    name = Column(String(255))
    comment = Column(String(255))
    settings = Column(String(255))
    image_url = Column(String(255))
    use_count = Column(Integer, default=0)
    access_token = Column(String(255), default="uuid()")
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

    id = Column(String(255), primary_key=True, default="uuid()")
    user_id = Column(String(255), ForeignKey('users.id'))
    service_type = Column(String(255))
    service_id = Column(String(255))
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")
    assistant_id = Column(String(255), ForeignKey('assistants.id'))

    user = relationship("User", back_populates="integrations")
    assistant = relationship("Assistant", back_populates="integrations")
    chats = relationship("Chat", back_populates="integration")
    managers = relationship("Manager", back_populates="integration")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(String(255), primary_key=True, default="uuid()")
    user_id = Column(String(255), ForeignKey('users.id'))
    manager_id = Column(String(255))
    client_id = Column(String(255), unique=True)
    assistant_id = Column(String(255))
    integration_id = Column(String(255))
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

    id = Column(String(255), primary_key=True, default="uuid()")
    user_id = Column(String(255), ForeignKey('users.id'))
    manager_id = Column(String(255), ForeignKey('managers.id'))
    chat_id = Column(String(255))
    name = Column(String(255))
    username = Column(String(255))
    image_url = Column(String(255))
    category = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    about = Column(String(255))
    company_name = Column(String(255))
    tags = Column(String(255))
    in_service_id = Column(String(255))
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    user = relationship("User", back_populates="clients")
    manager = relationship("Manager", back_populates="clients")
    chats = relationship("Chat", back_populates="client")


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(String(255), primary_key=True, default="uuid()")
    owner_id = Column(String(255), ForeignKey('users.id'))
    manager_id = Column(String(255))
    managed_by_id = Column(String(255), ForeignKey('users.id'))
    integration_id = Column(String(255), ForeignKey('integrations.id'))
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

    id = Column(String(255), primary_key=True, default="uuid()")
    chat_id = Column(String(255), ForeignKey('chats.id'))
    text = Column(String(255))
    files_url = Column(String(255))
    images_url = Column(String(255))
    incoming = Column(Boolean, default=True)
    from_assistant = Column(Boolean, default=False)
    from_user = Column(Boolean, default=False)
    from_manager = Column(Boolean, default=False)
    manager_id = Column(String(255))
    user_id = Column(String(255))
    assistant_id = Column(String(255))
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default="now()")
    created_at = Column(DateTime, default="now()")
    updated_at = Column(DateTime, onupdate="now()")

    chat = relationship("Chat", back_populates="messages")
    manager = relationship("Manager", back_populates="messages")
    user = relationship("User", back_populates="messages")
    assistant = relationship("Assistant", back_populates="messages")


Base.metadata.create_all(engine)
