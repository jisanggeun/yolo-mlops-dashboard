from pydantic import BaseModel

# Predict Response
class PredictResponse(BaseModel):
    filename: str # 파일 명
    predictions: list # Predict Result list
    message: str # 메세지
    image_path: str # image path