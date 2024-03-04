from .database import Session_, User, JivoBot,TelegramBot,TelegramUserBot,WhatsAppBot,
from models.schemas import EditProfileEntry


class Database:
    def __init__(self) -> None:
        self.db = Session_()

    async def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    async def update_profile(self, id: int, data: EditProfileEntry):
        user: User = self.db.query(User).filter(User.id == id).first()
        user.name = data.name
        user.phone = data.phone
        user.imageUrl = data.imageUrl
        user.telegram = data.telegram
        user.email = data.email
        user.company_name = data.company_name
        user.job_title = data.job_title
        self.db.commit()

    async def create_tg_bot(self,tgbot:):
        bot:TelegramBot = TelegramBot(
            project
        )

    async def get_jivo_bot(self, jivo_id: int) -> JivoBot:
        return self.db.query(JivoBot).filter(JivoBot.id == jivo_id).first()

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
