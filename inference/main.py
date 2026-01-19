from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import numpy as np
import cv2
import os

app = FastAPI(title="YOLO Inference Server")

# model load (TensorRT .engine or 일반 .pt model)
MODEL_PATH = os.getenv("MODEL_PATH", "yolov8n.pt")
model = YOLO(MODEL_PATH)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/predict")
async def predict(file: UploadFile=File(...)):
    # image read
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # inference
    results = model(img)

    # result parsing
    detections = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            detections.append({
                "class": int(box.cls[0]),
                "class_name": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    return {
        "detections": detections
    }

@app.get("/models")
def list_models():
    return {
        "current_model": MODEL_PATH
    }