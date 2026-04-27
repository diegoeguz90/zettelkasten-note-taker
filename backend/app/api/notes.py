from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models, schemas
from app.services import markdown

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@router.post("/", response_model=schemas.NoteDetailOut)
def create_note(note_in: schemas.NoteCreate, db: Session = Depends(get_db)):
    note_id = models.generate_uuid()
    content_path = markdown.save_note_content(note_id, note_in.content)
    
    db_note = models.Note(
        id=note_id,
        title=note_in.title,
        content_path=content_path
    )
    db.add(db_note)
    
    for target_id in note_in.connected_to_note_ids:
        target_note = db.query(models.Note).filter(models.Note.id == target_id).first()
        if target_note:
            connection = models.Connection(source_id=db_note.id, target_id=target_id)
            db.add(connection)
            
    db.commit()
    db.refresh(db_note)
    
    db_note.content = note_in.content
    return schemas.NoteDetailOut.model_validate(db_note)

@router.get("/{note_id}", response_model=schemas.NoteDetailOut)
def get_note(note_id: str, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    content = markdown.read_note_content(note_id)
    db_note.content = content
    return schemas.NoteDetailOut.model_validate(db_note)

@router.put("/{note_id}", response_model=schemas.NoteDetailOut)
def update_note(note_id: str, note_in: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db_note.title = note_in.title
    markdown.save_note_content(note_id, note_in.content)
    
    db.commit()
    db.refresh(db_note)
    
    db_note.content = note_in.content
    return schemas.NoteDetailOut.model_validate(db_note)
