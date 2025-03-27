from fastapi import FastAPI
from database import engine
from models import Base
from routes import router as chat_router
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    env_vars = {
        "CHATSUM_API": os.getenv("CHATSUM_API", "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"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", "postgres"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", "tiger"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB", "chatdb"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "5432")
    }
    for var, value in env_vars.items():
        print(f"{var}: {value}")

    yield  

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router, prefix="/chats")

@app.get("/")
def home():
    return {"message": "Hello Jee Aayan Here"}
