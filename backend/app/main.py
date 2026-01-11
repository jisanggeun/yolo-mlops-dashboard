from fastapi import FastAPI
from app.database import engine, Base
from app.api import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="YOLO MLOps Dashboard")

app.include_router(auth.router, prefix="/api", tags=["Auth"])

@app.get("/")
def root():
    return {
        "msg" : "YOLO MLOps API"
    }