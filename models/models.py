from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship, mapped_column
from DB.database import Base
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import Mapped


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(154), unique=True, index=True)
    username = Column(String(52), unique=True, index=True)
    email = Column(String(154), unique=True, index=True)
    password = Column(String(154))    # todo! password validation func
    hashed_password = Column(String(154))
    is_active = Column(Boolean, default=True)
    full_name = Column(String(154))
    company_name = Column(String(154))
    token = Column(String(154))
    expires = Column(DateTime())
    assistants: Mapped[list["Assistants"]] = relationship(
        "Assistants", back_populates="user")
    provider_id = Column(String(154))


class Assistants(Base):
    __tablename__ = "assistants"

    id = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["Users"] = relationship(back_populates="assistants")
    name = Column(String(154))
    settings = Column(String(4200))
    use_count = Column(BigInteger)
    comment = Column(String(154))
