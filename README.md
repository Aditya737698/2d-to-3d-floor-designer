# 🏠 2D to 3D Floor Designer

This project automatically converts 2D floor plan images into interactive 3D models using YOLOv8 for object detection and Three.js (`@react-three/fiber`) for visualization.

---

## 🚀 Features

- Upload 2D floor plans (JPG/PNG)
- Auto-detect walls, doors, windows, furniture using YOLOv8
- Export structured JSON data
- Render realistic 3D floor plan in a walkthrough viewer
- Built with React + FastAPI + Three.js + Ultralytics


## 🖥️ Running the Project Locally

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/Aditya737698/2d-to-3d-floor-designer.git
cd 2d-to-3d-floor-designer
```

### ⚙️2. Start the FastAPI Backend
```bash
cd floor-plan-object-detection
pip install -r requirements.txt  # Install dependencies

# Run backend API
uvicorn main:app --reload --port 8000
```
### 💻 3. Start the React Frontend
```bash
cd ../3d-floorplan-viewer
npm install
npm start
```
