from pydantic import BaseModel
from datetime import datetime

# Training task create request
class JobCreate(BaseModel):
    epochs: int = 100
    batch_size: int = 16

# Training task response
class JobResponse(BaseModel):
    id: int
    user_id: int
    status: str
    epochs: int
    batch_size: int
    created_at: datetime

    class Config:
        from_attributes=True



