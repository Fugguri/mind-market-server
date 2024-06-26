import asyncio
import uvicorn
from routers import *
from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware
from mics import jivo, tg, greenApi, utls
from models import schemas
# from DB.db import init_models
from dotenv import dotenv_values
envs = dotenv_values(".env")

mode = envs.get("MODE")

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
    "http://93.92.200.180:0"
    "https://93.92.200.180:0"
    "http://93.92.200.180"
    "https://93.92.200.180"

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

app.include_router(profile_router)
app.include_router(assistant_router)
app.include_router(integration_router)
app.include_router(crm_router)
app.include_router(chat_router)
app.include_router(webhooks_router)


if __name__ == "__main__":
    if mode == "DEV":
        uvicorn.run(app, host='0.0.0.0', port=8000)
    else:
        uvicorn.run(app, host='0.0.0.0', port=8000, root_path="/api_v2")
