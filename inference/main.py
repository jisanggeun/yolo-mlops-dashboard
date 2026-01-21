from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import numpy as np
import cv2
import os
import base64

app = FastAPI(title="YOLO Inference Server")

# model load (TensorRT .engine or 일반 .pt model)
MODEL_PATH = os.getenv("MODEL_PATH", "yolov8n.pt")
ENGINE_PATH = MODEL_PATH.replace(".pt", ".engine")

# tensorRT .engine 있으면 사용, 없으면 자동 convert
if os.path.exists(ENGINE_PATH):
    print(f"TensorRT Engine Load: {ENGINE_PATH}")
    model = YOLO(ENGINE_PATH)
else:
    print(f"TensorRT Converting: {MODEL_PATH} -> {ENGINE_PATH}")
    model = YOLO(MODEL_PATH)
    model.export(format="engine", device=0)
    model = YOLO(ENGINE_PATH)
    print("TensorRT Convert Complete")

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
    results = model(img, conf=0.7, iou=0.5)

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

    # visualize image create
    annotated_img = results[0].plot()

    # image base64 encoding
    _, buffer = cv2.imencode(".jpg", annotated_img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "detections": detections,
        "image_base64": img_base64
    }

@app.get("/models")
def list_models():
    return {
        "current_model": ENGINE_PATH if os.path.exists(ENGINE_PATH) else MODEL_PATH
    }