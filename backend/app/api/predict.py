from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from app.schemas.predict import PredictResponse
from app.services.auth import get_current_user
from ultralytics import YOLO
from datetime import datetime
from urllib.parse import unquote
import shutil
import os
import json

router = APIRouter()

# YOLO model 로드 (서버 시작 시 1번만)
model = YOLO("yolov8n.pt")

# Predict API (임시)
@router.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile=File(...), email: str=Depends(get_current_user)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    visualize_filename = f"visualize_{file.filename}"
    # 임시 file 저장
    temp_path = visualize_filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # YOLO Predict
    results = model(temp_path, conf=0.7, iou=0.5, save=True, project="runs", name=timestamp, exist_ok=True)

    # 결과 파싱
    predictions = []
    for result in results:
        for box in result.boxes:
            predictions.append({
                "class": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    # 원본 file 저장
    original_path = f"runs/{timestamp}/{file.filename}"
    shutil.copy(temp_path, original_path)

    # 임시 file 삭제
    os.remove(temp_path)

    # predictions JSON 저장
    json_path = f"runs/{timestamp}/result.json"
    with open(json_path, "w") as f:
        json.dump({
            "filename": file.filename,
            "visualize_filename": visualize_filename,
            "predictions": predictions
        }, f)

    return {
        "filename": file.filename,
        "predictions": predictions,
        "message": "예측 완료",
        "image_path": f"/api/predict/image/{timestamp}/{visualize_filename}"    
    }

# 과거 예측 목록 조회
@router.get("/predict/history")
async def get_predict_history(email: str=Depends(get_current_user)):
    history = []
    if os.path.exists("runs"):
        for timestamp in sorted(os.listdir("runs"), reverse=True):
            folder_path = f"runs/{timestamp}"
            json_path = f"{folder_path}/result.json"

            if os.path.isdir(folder_path) and os.path.exists(json_path):
                with open(json_path, "r") as f:
                    data = json.load(f)
                    
                history.append({
                    "timestamp": timestamp,
                    "filename": data["filename"],
                    "predictions": data["predictions"],
                    "image_path": f"/api/predict/image/{timestamp}/{data['visualize_filename']}"
                })
    return history

# 시각화 이미지 반환
@router.get("/predict/image/{timestamp}/{filename}")
async def get_predict_image(timestamp: str, filename: str):
    decoded_filename = unquote(filename)
    image_path = f"runs/{timestamp}/{decoded_filename}"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {
        "error": "이미지를 찾을 수 없습니다."
    }