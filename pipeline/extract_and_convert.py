# pipeline/extract_and_convert.py

import os
import json
from ultralytics import YOLO
from PIL import Image

# Define mapping of YOLO class indices to labels
CLASS_LABELS = {
    0: 'Column',
    1: 'Curtain Wall',
    2: 'Dimension',
    3: 'Door',
    4: 'Railing',
    5: 'Sliding Door',
    6: 'Stair Case',
    7: 'Wall',
    8: 'Window'
}

def detect_and_convert(image_path, output_dir="public/assets", model_path="floor-plan-object-detection/best.pt"):
    os.makedirs(output_dir, exist_ok=True)

    model = YOLO(model_path)
    results = model(image_path, conf=0.25)

    detections = []
    for box in results[0].boxes:
        cls_id = int(box.cls)
        label = CLASS_LABELS.get(cls_id, "Unknown")
        x1, y1, x2, y2 = map(float, box.xyxy[0])

        detections.append({
            "label": label,
            "position": {
                "x": (x1 + x2) / 2,
                "y": 0,
                "z": (y1 + y2) / 2
            },
            "size": {
                "width": abs(x2 - x1),
                "height": 20,
                "depth": abs(y2 - y1)
            }
        })

    # Save based on type
    grouped = {"walls": [], "doors": [], "windows": [], "furniture": []}
    for d in detections:
        l = d["label"].lower()
        if "wall" in l:
            grouped["walls"].append(d)
        elif "door" in l:
            grouped["doors"].append(d)
        elif "window" in l:
            grouped["windows"].append(d)
        else:
            grouped["furniture"].append(d)

    for key, data in grouped.items():
        json_path = os.path.join(output_dir, f"{key}.json")
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

    print(f"✅ JSON files saved to {output_dir}")

# Example run
if __name__ == "__main__":
    detect_and_convert("pipeline/example2.png")