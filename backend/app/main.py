from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, job
from app.api import auth, jobs, predict, monitor
from prometheus_fastapi_instrumentator import Instrumentator

# table 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="YOLO MLOps Dashboard")

# Prometheus Metric 노출
Instrumentator().instrument(app).expose(app)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React 주소 (허용할 주소)
    allow_credentials=True, # 쿠키/인증 허용
    allow_methods=["*"], # 모든 HTTP method 허용 (GET, POST ...)
    allow_headers=["*"], # 모든 헤더 허용 
)

app.include_router(auth.router, prefix="/api", tags=["Auth"]) # 회원가입, 로그인
app.include_router(jobs.router, prefix="/api", tags=["Jobs"]) # Training API
app.include_router(predict.router, prefix="/api", tags=["Predict"]) # Predict API
app.include_router(monitor.router, prefix="/api", tags=["monitor"]) # monitor API

@app.get("/")
def root():
    return {
        "msg" : "YOLO MLOps API"
    }