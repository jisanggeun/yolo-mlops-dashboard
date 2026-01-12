from pydantic import BaseModel

# Predict Response
class PredictResponse(BaseModel):
    filename: str
    predictions: list # 추후, YOLO result 형식으로 변경
    message: str="임시 응답"