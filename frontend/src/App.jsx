import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import GraphView from './components/GraphView';
import api from './api';

function App() {
  const [apiKey, setApiKey] = useState('');

  useEffect(() => {
    api.get('/settings/api-key').then(res => {
      setApiKey(res.data.api_key);
    }).catch(err => console.error("Could not load API Key", err));
  }, []);

  return (
    <div className="w-full min-h-screen">
      <nav className="navbar">
        <h2 style={{margin:0}}>ZNT <span style={{fontSize:'0.5em', color:'#aaa'}}>Zettelkasten</span></h2>
        <div className="flex gap-4 items-center">
          <Link to="/" style={{color: 'white', textDecoration: 'none'}}>Dashboard</Link>
          <Link to="/graph" style={{color: 'white', textDecoration: 'none'}}>Graph View</Link>
          <span style={{background: '#334155', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem'}}>
            MCP Key: {apiKey ? `${apiKey.substring(0, 8)}...` : 'Loading...'}
          </span>
        </div>
      </nav>
      
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/graph" element={<GraphView />} />
      </Routes>
    </div>
  );
}

export default App;
