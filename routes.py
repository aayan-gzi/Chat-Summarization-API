import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from database import get_db
from models import ChatMessage
from pydantic import BaseModel
from datetime import datetime

load_dotenv()
OPENROUTER_API_KEY = os.getenv("CHATSUM_API")
if not OPENROUTER_API_KEY:
    raise RuntimeError("API Key not found. Check your .env file!")

router = APIRouter()

class ChatCreate(BaseModel):
    user_id: str
    conversation_id: str
    message: str

class SummarizeRequest(BaseModel):
    conversation_id: str

@router.post("/chats")
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db)):
    new_chat = ChatMessage(
        user_id=chat.user_id,
        conversation_id=chat.conversation_id,
        message=chat.message,
        timestamp=datetime.utcnow()
    )
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return {"message": "Chat stored successfully", "chat": new_chat}

@router.get("/chats/{conversation_id}")
async def get_chats(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatMessage).filter(ChatMessage.conversation_id == conversation_id))
    chats = result.scalars().all()
    
    if not chats:
        return {"message": "No chats found for this conversation"}
    
    return {"conversation_id": conversation_id, "chats": chats}

@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatMessage).filter(ChatMessage.id == chat_id))
    chat = result.scalars().first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    await db.execute(delete(ChatMessage).where(ChatMessage.id == chat_id))
    await db.commit()

    return {"message": f"Chat {chat_id} deleted successfully"}

@router.post("/chats/summarize")
async def summarize_chat(request: SummarizeRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatMessage).filter(ChatMessage.conversation_id == request.conversation_id))
    chats = result.scalars().all()

    if not chats:
        raise HTTPException(status_code=404, detail="No chats found for this conversation")

    chat_text = "\n".join([chat.message for chat in chats])

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            json={
                "model": "mistral",
                "messages": [
                    {"role": "system", "content": "Summarize the following conversation:"},
                    {"role": "user", "content": chat_text}
                ]
            }
        )
        response_json = response.json()
        summary = response_json["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in summarization: {str(e)}")

    return {"conversation_id": request.conversation_id, "summary": summary}

@router.get("/users/{user_id}")
async def get_user_chats(user_id: str, page: int = 1, limit: int = 10, db: AsyncSession = Depends(get_db)):
    print(f"Fetching chats for user: {user_id}, page: {page}, limit: {limit}")
    
    offset = (page - 1) * limit
    
    result = await db.execute(
        select(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.timestamp.desc())
        .offset(offset)
        .limit(limit)
    )
    chats = result.scalars().all()

    total_chats_result = await db.execute(
        select(ChatMessage).filter(ChatMessage.user_id == user_id)
    )
    total_chats = len(total_chats_result.scalars().all())

    return {
        "user_id": user_id,
        "page": page,
        "limit": limit,
        "total_chats": total_chats,
        "total_pages": (total_chats // limit) + (1 if total_chats % limit > 0 else 0),
        "chats": chats
    }
