from fastapi import FastAPI
from app.database import engine, Base
from app.api import auth, jobs, predict

# table 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="YOLO MLOps Dashboard")

app.include_router(auth.router, prefix="/api", tags=["Auth"]) # 회원가입, 로그인
app.include_router(jobs.router, prefix="/api", tags=["Jobs"]) # Training API
app.include_router(predict.router, prefix="/api", tags=["Predict"]) # Predict API

@app.get("/")
def root():
    return {
        "msg" : "YOLO MLOps API"
    }