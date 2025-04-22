from sqlalchemy import Boolean, Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_completed = Column(Boolean, default=False)
