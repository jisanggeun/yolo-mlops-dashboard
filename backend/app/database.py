from sqlalchemy import create_engine # DB 연결 생성
from sqlalchemy.ext.declarative import declarative_base # 테이블 모델 기본 class
from sqlalchemy.orm import sessionmaker # DB 세션 생성기
from app.config import settings

# DB 엔진 생성
engine = create_engine(settings.DATABASE_URL)

# 세션 생성
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 베이스 class
Base = declarative_base()

def get_db():
    db = session_local() # 세션 열기
    try:
        yield db # API에서 사용
    finally:
        db.close() # 요청 끝나면 세션 닫기