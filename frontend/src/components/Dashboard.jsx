import React, { useState, useEffect } from 'react';
import api from '../api';
import NoteEditor from './NoteEditor';

export default function Dashboard() {
  const [notes, setNotes] = useState([]);
  const [activeNote, setActiveNote] = useState(null);
  const [isCreating, setIsCreating] = useState(false);

  const fetchNotes = async () => {
    try {
      const res = await api.get('/notes');
      setNotes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleCreate = () => {
    setActiveNote(null);
    setIsCreating(true);
  };

  const handleNoteClick = async (id) => {
    try {
      const res = await api.get(`/notes/${id}`);
      setActiveNote(res.data);
      setIsCreating(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (noteData) => {
    try {
      if (isCreating) {
        await api.post('/notes', noteData);
      } else {
        await api.put(`/notes/${activeNote.id}`, noteData);
      }
      setIsCreating(false);
      fetchNotes();
      if (!isCreating) {
        handleNoteClick(activeNote.id);
      } else {
        setActiveNote(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-grid">
      <div className="sidebar glass-panel">
        <div className="flex gap-2">
          <button className="w-full" onClick={handleCreate}>+ New Note</button>
        </div>
        <div className="mt-4 flex-col gap-2" style={{marginTop: '1rem'}}>
          <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>Library</h3>
          {notes.map(note => (
            <div 
              key={note.id} 
              className={`note-item ${activeNote?.id === note.id ? 'active' : ''}`}
              onClick={() => handleNoteClick(note.id)}
            >
              <h4>{note.title}</h4>
              <p>{new Date(note.created_at).toLocaleDateString()}</p>
            </div>
          ))}
          {notes.length === 0 && <p style={{color: '#94a3b8', fontSize: '0.9rem'}}>No notes yet.</p>}
        </div>
      </div>

      <div className="main-content glass-panel" style={{display: 'flex', flexDirection: 'column'}}>
        {(activeNote || isCreating) ? (
          <NoteEditor 
            note={activeNote} 
            onSave={handleSave} 
            allNotes={notes}
          />
        ) : (
          <div className="flex h-full items-center" style={{justifyContent: 'center', color: '#64748b'}}>
            Select a note or create a new one to begin.
          </div>
        )}
      </div>

      <div className="right-panel glass-panel">
        <h3>Connections</h3>
        {activeNote ? (
          <div>
            <p style={{fontSize: '0.9rem', color: '#94a3b8'}}>
              Notes connected to <strong>{activeNote.title}</strong>:
            </p>
            <ul style={{paddingLeft: '1rem', marginTop: '0.5rem', fontSize: '0.9rem'}}>
              {activeNote.outgoing_connections?.map(c => {
                const target = notes.find(n => n.id === c.target_id);
                return <li key={c.id}>&rarr; {target?.title || c.target_id}</li>
              })}
              {activeNote.incoming_connections?.map(c => {
                const source = notes.find(n => n.id === c.source_id);
                return <li key={c.id}>&larr; {source?.title || c.source_id}</li>
              })}
            </ul>
            {(activeNote.outgoing_connections?.length === 0 && activeNote.incoming_connections?.length === 0) && (
              <p style={{fontSize: '0.8rem', color: '#64748b'}}>No connections yet.</p>
            )}
          </div>
        ) : (
          <p style={{fontSize: '0.9rem', color: '#64748b'}}>Select a note to view connections.</p>
        )}
      </div>
    </div>
  );
}
