from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    conversation_id = Column(String, index=True)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
