from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import models, schemas

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/api-key", response_model=schemas.SettingsOut)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(api_key=str(uuid.uuid4()))
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.post("/api-key", response_model=schemas.SettingsOut)
def generate_api_key(db: Session = Depends(get_db)):
    settings = db.query(models.Settings).first()
    if not settings:
        settings = models.Settings(api_key=str(uuid.uuid4()))
        db.add(settings)
    else:
        settings.api_key = str(uuid.uuid4())
    db.commit()
    db.refresh(settings)
    return settings
