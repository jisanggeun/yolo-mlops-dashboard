from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base

# User 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    profile_image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # datetime.utcnow를 사용 안하는 이유
	# utcnow()는 deprecated(더 이상 사용하지 않음) 상태임