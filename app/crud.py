from sqlalchemy.orm import Session
from app import models
from app import schemas


def get_entry(db: Session, entry_id: int):
    return db.query(models.Entry).filter(models.Entry.id == entry_id).first()


def get_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entry).offset(skip).limit(limit).all()


def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_entry(db: Session, entry_id: int, entry: schemas.EntryUpdate):
    db_entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if db_entry:
        update_data = entry.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_entry, key, value)
        db.commit()
        db.refresh(db_entry)
    return db_entry


def delete_entry(db: Session, entry_id: int):
    db_entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
    return db_entry


def mark_entry_completed(db: Session, entry_id: int):
    db_entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if db_entry and not db_entry.completed:
        db_entry.is_completed = True
        db.commit()
        db.refresh(db_entry)
    return db_entry
