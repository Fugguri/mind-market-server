from fastapi import FastAPI
from routers import *
import uvicorn
from prisma_ import prisma
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="MindMarketAPI",
    summary="",
    version="0.0.1",
    description="Your AI assistant",
)


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("starting up!")
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/", name="Wellcome", tags=["Основное"], description="Тут будет описание методов?")
async def user():
    return {"message": "Wellcome to MindMarketAPI"}



app.include_router(profile_router)
app.include_router(assistant_router)
app.include_router(integration_router)
app.include_router(crm_router)
app.include_router(chat_router)

if __name__ == "__main__":

    uvicorn.run(app, host='0.0.0.0', port=7000)
