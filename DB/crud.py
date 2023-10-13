from sqlalchemy.orm import Session
from models import models, schemas



async def get_user(db:Session,user_id:int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

async def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

async def verify_token(db: Session, token: str):
    
    return db.query(models.Users).filter(models.Users.token == token).first()

async def create_user(db: Session, user: schemas.User):
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



async def get_assistants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Assistants).offset(skip).limit(limit).all()

async def create_user_assistant(db: Session, assistant: schemas.Assistant,):
    db_item = models.Assistants(**assistant.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

async def update_assistant_count(db:Session,assistant:models.Assistants):
    
    re = db.query(models.Assistants).filter(models.Assistants.id == assistant.id).update({models.Assistants.use_count : assistant.use_count + 1})
    db.commit()
    print(re,{models.Assistants.use_count : assistant.use_count + 1})
    return re   