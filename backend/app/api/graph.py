from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models, schemas

router = APIRouter(prefix="/api/graph", tags=["graph"])

@router.get("/", response_model=schemas.GraphOut)
def get_graph(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    connections = db.query(models.Connection).all()
    
    nodes = [schemas.GraphNode(id=note.id, label=note.title) for note in notes]
    edges = [schemas.GraphEdge(id=conn.id, source=conn.source_id, target=conn.target_id) for conn in connections]
    
    return schemas.GraphOut(nodes=nodes, edges=edges)

@router.post("/connections", response_model=schemas.ConnectionOut)
def create_connection(conn_in: schemas.ConnectionBase, db: Session = Depends(get_db)):
    source = db.query(models.Note).filter(models.Note.id == conn_in.source_id).first()
    target = db.query(models.Note).filter(models.Note.id == conn_in.target_id).first()
    
    if not source or not target:
        raise HTTPException(status_code=404, detail="Source or target note not found")
        
    db_conn = models.Connection(source_id=conn_in.source_id, target_id=conn_in.target_id)
    db.add(db_conn)
    db.commit()
    db.refresh(db_conn)
    return db_conn
