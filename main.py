import uvicorn
from routers import *
from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware
from mics import jivo, tg, greenApi, utls
from models import schemas

app = FastAPI(
    title="MindMarketAPI",
    summary="",
    version="0.1.1",
    description="Your AI assistant",
)


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://web-mindmarket",

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", name="Wellcome", tags=["Основное"], description="Тут будет описание методов?")
async def user():
    return {"message": "Wellcome to MindMarketAPI"}


@app.post("/integrations/tgbot", name="Добавление Telegram бота", description="Добавление бота, созданного в BotFather ", tags=["Интеграции"])
async def create_tg_bot(tgbot: schemas.TgBotEntry):
    print(tgbot)
    bot = tg.TgBot(tgbot.token)
    me = await bot.getInfo()
    print(me)
    await bot.setWebhook(tgbot.token)
    # tg_bot_model = await db.get_telegrambot(bot_id=bot_id)
    # await messages.handle_telegrambot_message(json_request, tg_bot_model)
# app.add_middleware()

app.include_router(profile_router)
app.include_router(assistant_router)
app.include_router(integration_router)
app.include_router(crm_router)
app.include_router(chat_router)
app.include_router(webhooks_router)


if __name__ == "__main__":

    uvicorn.run(app, host='0.0.0.0', port=8000, root_path="/api_v2")
