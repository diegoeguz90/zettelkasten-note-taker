from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SettingsBase(BaseModel):
    api_key: str

class SettingsOut(SettingsBase):
    id: int

    class Config:
        from_attributes = True

class ConnectionBase(BaseModel):
    source_id: str
    target_id: str

class ConnectionOut(ConnectionBase):
    id: str

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str

class NoteCreate(NoteBase):
    content: str
    connected_to_note_ids: Optional[List[str]] = []

class NoteOut(NoteBase):
    id: str
    content_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoteDetailOut(NoteOut):
    content: str
    outgoing_connections: List[ConnectionOut] = []
    incoming_connections: List[ConnectionOut] = []

class GraphNode(BaseModel):
    id: str
    label: str

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str

class GraphOut(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
