import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

export default function NoteEditor({ note, onSave, allNotes }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedConnections, setSelectedConnections] = useState([]);
  const [isPreview, setIsPreview] = useState(false);

  useEffect(() => {
    if (note) {
      setTitle(note.title);
      setContent(note.content || '');
      setSelectedConnections([]);
    } else {
      setTitle('');
      setContent('');
      setSelectedConnections([]);
    }
  }, [note]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      title,
      content,
      connected_to_note_ids: selectedConnections
    });
  };

  const handleConnectionToggle = (id) => {
    if (selectedConnections.includes(id)) {
      setSelectedConnections(selectedConnections.filter(c => c !== id));
    } else {
      setSelectedConnections([...selectedConnections, id]);
    }
  };

  return (
    <div className="flex-col h-full">
      <div className="flex justify-between items-center" style={{marginBottom: '1rem'}}>
        <h2>{note ? 'Edit Note' : 'Create New Note'}</h2>
        <button className="secondary" type="button" onClick={() => setIsPreview(!isPreview)}>
          {isPreview ? 'Edit Mode' : 'Preview Mode'}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex-col h-full" style={{flex: 1}}>
        <input 
          type="text" 
          placeholder="Note Title" 
          value={title} 
          onChange={e => setTitle(e.target.value)} 
          required 
          style={{fontSize: '1.2rem', fontWeight: 'bold'}}
        />

        {isPreview ? (
          <div style={{flex: 1, padding: '1rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', overflowY: 'auto', marginBottom: '1rem'}}>
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        ) : (
          <textarea 
            placeholder="Write your markdown here..." 
            value={content} 
            onChange={e => setContent(e.target.value)} 
            style={{flex: 1, resize: 'none', fontFamily: 'monospace'}}
            required
          />
        )}

        {!note && (
          <div style={{marginBottom: '1rem'}}>
            <h4 style={{marginBottom: '0.5rem', fontSize: '0.9rem', color: '#94a3b8'}}>Connect to existing notes:</h4>
            <div className="flex flex-wrap" style={{gap: '0.5rem'}}>
              {allNotes.map(n => (
                <div 
                  key={n.id} 
                  onClick={() => handleConnectionToggle(n.id)}
                  style={{
                    padding: '0.2rem 0.6rem', 
                    borderRadius: '16px', 
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    background: selectedConnections.includes(n.id) ? '#3b82f6' : 'rgba(255,255,255,0.1)',
                    border: '1px solid rgba(255,255,255,0.2)'
                  }}
                >
                  {n.title}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex" style={{justifyContent: 'flex-end', marginTop: 'auto'}}>
          <button type="submit">Save Note</button>
        </div>
      </form>
    </div>
  );
}
