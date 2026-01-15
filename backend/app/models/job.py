from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime, timezone
from app.database import Base

# Job 테이블 정의
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # task 요청한 user
    status = Column(String(20), default="pending") # status flow: pending -> running -> completed or failed 
    epochs = Column(Integer, default=100) # training epochs
    batch_size = Column(Integer, default=16)
    progress = Column(Float, default=0.0) # 진행도 (0 ~ 100)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))