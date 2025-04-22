from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import crud
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/entries/", response_model=schemas.Entry)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db=db, entry=entry)


@app.get("/entries/", response_model=list[schemas.Entry])
def read_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entries = crud.get_entries(db, skip=skip, limit=limit)
    return entries


@app.get("/entries/{entry_id}", response_model=schemas.Entry)
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud.get_entry(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry


@app.put("/entries/{entry_id}", response_model=schemas.Entry)
def update_entry(entry_id: int, entry: schemas.EntryUpdate, db: Session = Depends(get_db)):
    db_entry = crud.update_entry(db, entry_id=entry_id, entry=entry)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry


@app.delete("/entries/{entry_id}", response_model=schemas.Entry)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud.delete_entry(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry


@app.patch("/entries/{entry_id}/complete", response_model=schemas.Entry)
def mark_entry_completed(entry_id: int, db: Session = Depends(get_db)):
    db_entry = crud.mark_entry_completed(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry
