from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, index=True)
    content_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    outgoing_connections = relationship("Connection", foreign_keys="[Connection.source_id]", back_populates="source_note")
    incoming_connections = relationship("Connection", foreign_keys="[Connection.target_id]", back_populates="target_note")

class Connection(Base):
    __tablename__ = "connections"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, ForeignKey("notes.id"))
    target_id = Column(String, ForeignKey("notes.id"))

    source_note = relationship("Note", foreign_keys=[source_id], back_populates="outgoing_connections")
    target_note = relationship("Note", foreign_keys=[target_id], back_populates="incoming_connections")

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, default=1)
    api_key = Column(String, unique=True, index=True)
