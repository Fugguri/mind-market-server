from .database import Session, User
from models import schemas


class Database:
    def __init__(self) -> None:
        ...

    async def get_user(user_id: int, db: Session = Session):
        return db.query(User).filter(User.id == user_id).first()

    # async def get_users(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.Users).offset(skip).limit(limit).all()

    # async def get_user_by_username(db: Session, username: str):
    #     return db.query(models.Users).filter(models.Users.username == username).first()

    # async def verify_token(db: Session, token: str):
    #     return db.query(models.Users).filter(models.Users.token == token).first()

    # async def get_assistants(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.Assistants).offset(skip).limit(limit).all()

    # async def get_assistants(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.Assistants).offset(skip).limit(limit).all()

    # async def create_user_assistant(db: Session, assistant: schemas.Assistant,):
    #     db_item = models.Assistants(**assistant.dict())
    #     db.add(db_item)
    #     db.commit()
    #     db.refresh(db_item)
    #     return db_item

    # async def update_assistant_count(db: Session, assistant):

    #     re = db.query(models.Assistants).filter(models.Assistants.id == assistant.id).update(
    #         {models.Assistants.use_count: assistant.use_count + 1})
    #     db.commit()
    #     print(re, {models.Assistants.use_count: assistant.use_count + 1})
    #     return re
