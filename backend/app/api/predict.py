from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from app.schemas.predict import PredictResponse
from app.services.auth import get_current_user
from ultralytics import YOLO
from datetime import datetime
import shutil
import os

router = APIRouter()

# YOLO model 로드 (서버 시작 시 1번만)
model = YOLO("yolov8n.pt")

# Predict API (임시)
@router.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile=File(...), email: str=Depends(get_current_user)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 임시 file 저장
    temp_path = f"temp_{file.filename}"
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

    # 임시 file 삭제
    os.remove(temp_path)

    return {
        "filename": file.filename,
        "predictions": predictions,
        "message": "예측 완료",
        "image_path": f"/api/predict/image/{timestamp}/{file.filename}"    
    }

# 과거 예측 목록 조회
@router.get("/predict/history")
async def get_predict_history(email: str=Depends(get_current_user)):
    history = []
    if os.path.exists("runs"):
        for timestamp in sorted(os.listdir("runs"), reverse=True):
            folder_path = f"runs/{timestamp}"
            if os.path.isdir(folder_path):
                for filename in os.listdir(folder_path):
                    history.append({
                        "timestamp": timestamp,
                        "filename": filename,
                        "image_path": f"/api/predict/image/{timestamp}/{filename}"
                    })
    return history

# 시각화 이미지 반환
@router.get("/predict/image/{timestamp}/{filename}")
async def get_predict_image(timestamp: str, filename: str):
    image_path = f"runs/{timestamp}/{filename}"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    return {
        "error": "이미지를 찾을 수 없습니다."
    }