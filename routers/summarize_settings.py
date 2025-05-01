from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from connections.cnx import SessionLocal
from models.summarize_settings import SummarizeSettings as SummarizeSettingsModel

# Dependency to get DB session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class SummarizeBase(BaseModel):
    file_path: str
    text: str
    link: str

class SummarizeCreate(SummarizeBase):
    pass

class SummarizeUpdate(BaseModel):
    file_path: Optional[str] = None
    text: Optional[str] = None
    link: Optional[str] = None

class SummarizeRead(SummarizeBase):
    id: int

    class Config:
        orm_mode = True

class SummarizeSettings:
    """
    Class-based CRUD for summarize settings.
    """
    def __init__(self):
        self.router = APIRouter(prefix="/summarize/files", tags=["files"])

        # Register routes
        self.router.post("/", response_model=SummarizeRead)(self.create_summarize)
        self.router.get("/{id}", response_model=SummarizeRead)(self.read_summarize)
        self.router.get("/", response_model=List[SummarizeRead])(self.read_all_summarizes)
        self.router.put("/{id}", response_model=SummarizeRead)(self.update_summarize)
        self.router.delete("/{id}")(self.delete_summarize)

    def create_summarize(self, summarize: SummarizeCreate, db: Session = Depends(get_db_session)):
        db_obj = SummarizeSettingsModel(**summarize.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_summarize(self, id: int, db: Session = Depends(get_db_session)):
        obj = db.get(SummarizeSettingsModel, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Summarize not found")
        return obj

    def read_all_summarizes(self, db: Session = Depends(get_db_session)):
        return db.query(SummarizeSettingsModel).all()

    def update_summarize(self, id: int, update: SummarizeUpdate, db: Session = Depends(get_db_session)):
        obj = db.get(SummarizeSettingsModel, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Summarize not found")
        for field, value in update.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete_summarize(self, id: int, db: Session = Depends(get_db_session)):
        obj = db.get(SummarizeSettingsModel, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Summarize not found")
        db.delete(obj)
        db.commit()
        return {"detail": "Summarize deleted"}

# Instantiate and expose router
summarize_settings = SummarizeSettings()
router = summarize_settings.router
