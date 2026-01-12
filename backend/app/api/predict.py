from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.predict import PredictResponse
from app.services.auth import get_current_user

router = APIRouter()

# Predict API (임시)
@router.post("/predict", response_model=PredictResponse)
async def predict(file: UploadFile=File(...), email: str=Depends(get_current_user)):
    # 임시 response
    return {
        "filename": file.filename,
        "predictions": [{
            "class": "person", # object class
            "confidence": 0.95, # confidence score
            "bbox": [100, 100, 200, 200] # bounding box
        }, {
            "class": "car",
            "confidence": 0.87,
            "bbox": [300, 150, 450, 300]
        }],
        "message": "임시 응답 (Inference Server 연결 후 바꿀 예정)"
    }