import streamlit as st
from ultralytics import YOLO
import PIL
import helper
import setting
import torch
from torch.serialization import add_safe_globals
import json
import os
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from io import BytesIO

# FastAPI setup
app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safe globals for PyTorch 2.6+
from ultralytics.nn.modules.block import DFL, C2f, Bottleneck, SPPF
from ultralytics.nn.tasks import DetectionModel
from ultralytics.nn.modules.conv import Conv, Concat
from ultralytics.nn.modules.head import Detect
from ultralytics.utils import IterableSimpleNamespace
from ultralytics.utils.loss import v8DetectionLoss, BboxLoss
from ultralytics.utils.tal import TaskAlignedAssigner
from torch.nn.modules.loss import BCEWithLogitsLoss
from torch.nn.modules.container import Sequential, ModuleList
from torch.nn import Conv2d, BatchNorm2d, ReLU, Upsample, MaxPool2d, Sigmoid, SiLU

add_safe_globals([
    DetectionModel, Sequential, ModuleList,
    Conv, Concat, C2f, Bottleneck, SPPF,
    Conv2d, BatchNorm2d, ReLU, Upsample, MaxPool2d, Sigmoid, SiLU,
    Detect, DFL, IterableSimpleNamespace,
    v8DetectionLoss, BCEWithLogitsLoss, TaskAlignedAssigner, BboxLoss
])

model = YOLO("best.pt")

@app.get("/")
def read_root():
    return {"message": "YOLOv8 Floor Plan API is running"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    results = model.predict(image, conf=0.3)
    boxes = results[0].boxes
    names = model.names

    label_data = {"Wall": [], "Door": [], "Window": [], "Furniture": []}

    for box in boxes:
        cls_id = int(box.cls)
        label = names[cls_id]
        xyxy = box.xyxy[0].tolist()

        item = {
            "x": float((xyxy[0] + xyxy[2]) / 2),
            "y": float((xyxy[1] + xyxy[3]) / 2),
            "width": float(abs(xyxy[2] - xyxy[0])),
            "height": float(abs(xyxy[3] - xyxy[1]))
        }

        if label == "Wall":
            label_data["Wall"].append(item)
        elif label in ["Door", "Sliding Door"]:
            label_data["Door"].append(item)
        elif label == "Window":
            label_data["Window"].append(item)
        elif label in ["Stair Case", "Column", "Curtain Wall", "Railing"]:
            label_data["Furniture"].append(item)

    # Update JSON files inside frontend/public/assets
    assets_dir = "../3d-floorplan-viewer/public/assets"
    os.makedirs(assets_dir, exist_ok=True)

    with open(os.path.join(assets_dir, "walls.json"), "w") as f:
        json.dump(label_data["Wall"], f, indent=2)
    with open(os.path.join(assets_dir, "doors.json"), "w") as f:
        json.dump(label_data["Door"], f, indent=2)
    with open(os.path.join(assets_dir, "windows.json"), "w") as f:
        json.dump(label_data["Window"], f, indent=2)
    with open(os.path.join(assets_dir, "furniture.json"), "w") as f:
        json.dump(label_data["Furniture"], f, indent=2)

    return JSONResponse(content={"status": "success", "message": "Detection complete. Viewer updated."})

# Optional: Streamlit manual UI
def main():
    setting.configure_page()
    with st.sidebar:
        st.header("Image Configuration")
        source_img = st.file_uploader("Choose an image...", type=("jpg", "jpeg", "png"))
        confidence = setting.get_model_confidence()
        available_labels = ['Column', 'Curtain Wall', 'Dimension', 'Door', 'Railing',
                            'Sliding Door', 'Stair Case', 'Wall', 'Window']
        selected_labels = setting.select_labels(available_labels)

    st.title("Floor Plan Object Detection using YOLOv8")
    col1, col2 = st.columns(2)
    uploaded_image = None

    with col1:
        if source_img:
            uploaded_image = PIL.Image.open(source_img)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        else:
            st.warning("Please upload an image.")

    if st.sidebar.button('Detect Objects') and uploaded_image:
        res = model.predict(uploaded_image, conf=confidence)
        filtered_boxes = [box for box in res[0].boxes if model.names[int(box.cls)] in selected_labels]
        res[0].boxes = filtered_boxes
        res_plotted = res[0].plot()[:, :, ::-1]
        with col2:
            st.image(res_plotted, caption='Detected Image', use_column_width=True)
            object_counts = helper.count_detected_objects(model, filtered_boxes)
            st.write("### Detected Objects and their Counts:")
            for label, count in object_counts.items():
                st.write(f"- **{label}**: {count}")
            csv_file = helper.generate_csv(object_counts)
            st.download_button(
                label="📅 Download CSV",
                data=csv_file,
                file_name='detected_objects.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()