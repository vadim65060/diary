from datetime import datetime
from pydantic import BaseModel


class EntryBase(BaseModel):
    title: str
    description: str | None = None


class EntryCreate(EntryBase):
    pass


class EntryUpdate(EntryBase):
    is_completed: bool | None = None


class Entry(EntryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_completed: bool

    class Config:
        from_attributes = True
