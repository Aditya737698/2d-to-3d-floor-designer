// src/App.js
import React, { useEffect, useState } from 'react';
import FloorPlanViewer from './components/FloorPlanViewer.jsx';
import FileUpload from './components/FileUpload.jsx'; // ✅ New import
import './App.css';

function App() {
  const [walls, setWalls] = useState([]);
  const [doors, setDoors] = useState([]);
  const [windows, setWindows] = useState([]);
  const [furniture, setFurniture] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJSON = async (filename, setter) => {
      try {
        const res = await fetch(`/assets/${filename}.json`);
        if (!res.ok) throw new Error(`${filename} fetch failed`);
        const data = await res.json();
        setter(data);
      } catch (err) {
        console.error(`Error loading ${filename}.json`, err);
      }
    };

    const loadAll = async () => {
      await Promise.all([
        fetchJSON('walls', setWalls),
        fetchJSON('doors', setDoors),
        fetchJSON('windows', setWindows),
        fetchJSON('furniture', setFurniture),
      ]);
      setLoading(false);
    };

    loadAll();
  }, []);

  return (
    <div className="App">
      <h1>🏠 Auto Floor Plan Viewer</h1>

      {/* ✅ Upload Component */}
      <FileUpload onSuccess={() => window.location.reload()} />

      {/* 3D Viewer */}
      {loading ? <p>Loading 3D layout...</p> : (
        <FloorPlanViewer 
          walls={walls} 
          doors={doors} 
          windows={windows} 
          furniture={furniture} 
        />
      )}
    </div>
  );
}

export default App;