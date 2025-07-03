// src/components/FloorPlanViewer.jsx
import React, { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, Sky, PerspectiveCamera } from '@react-three/drei';

const Wall = ({ x, y, width, height }) => {
  const length = Math.max(width, height);
  const thickness = Math.min(width, height);
  const rotationY = width > height ? 0 : Math.PI / 2;

  return (
    <mesh position={[x, 50, y]} rotation={[0, rotationY, 0]} castShadow receiveShadow>
      <boxGeometry args={[length, 100, thickness || 1]} />
      <meshStandardMaterial color="#888888" roughness={0.7} metalness={0.1} />
    </mesh>
  );
};

const StructureBox = ({ x, y, width, height, color }) => {
  if ([x, y, width, height].some(v => typeof v !== 'number' || isNaN(v))) return null;

  return (
    <mesh position={[x, 25, y]} castShadow receiveShadow>
      <boxGeometry args={[width, 50, height]} />
      <meshStandardMaterial color={color} roughness={0.5} metalness={0.2} />
    </mesh>
  );
};

const FloorPlan = () => {
  const [walls, setWalls] = useState([]);
  const [doors, setDoors] = useState([]);
  const [windows, setWindows] = useState([]);
  const [furniture, setFurniture] = useState([]);

  useEffect(() => {
    const fetchJSON = async (file, setter) => {
      try {
        const res = await fetch(`/assets/${file}`);
        const data = await res.json();
        setter(data);
      } catch (err) {
        console.error(`Error loading ${file}:`, err);
      }
    };

    fetchJSON('walls.json', setWalls);
    fetchJSON('doors.json', setDoors);
    fetchJSON('windows.json', setWindows);
    fetchJSON('furniture.json', setFurniture);
  }, []);

  return (
    <>
      {/* Ground */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[5000, 5000]} />
        <meshStandardMaterial color="#f0f0f0" />
      </mesh>

      {/* Structures */}
      {walls.map((w, i) => (
        <Wall key={`wall-${i}`} {...w} />
      ))}
      {doors.map((d, i) => (
        <StructureBox key={`door-${i}`} {...d} color="#8B4513" />
      ))}
      {windows.map((w, i) => (
        <StructureBox key={`window-${i}`} {...w} color="#87CEEB" />
      ))}
      {furniture.map((f, i) => (
        <StructureBox key={`furn-${i}`} {...f} color="#9b59b6" />
      ))}
    </>
  );
};

export default function FloorPlanViewer() {
  return (
    <Canvas shadows camera={{ position: [0, 500, 1000], fov: 55 }}>
      <ambientLight intensity={0.4} />
      <directionalLight
        position={[300, 400, 300]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <Sky sunPosition={[100, 50, 100]} />
      <Environment preset="sunset" background={false} />
      <FloorPlan />
      <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
    </Canvas>
  );
}