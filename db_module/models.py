# db_module/models.py
from sqlalchemy import Column, String, DateTime, func
from .db_config import Base
from pydantic import BaseModel

class Messages(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, index=True)
    thread_ts = Column(String)
    user = Column(String)
    text = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class SlackMessage(BaseModel):
    id: str
    username: str
    email: str
    channel: str
    message: str
