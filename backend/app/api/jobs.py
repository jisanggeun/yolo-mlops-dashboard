from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.services.auth import get_current_user
from app.tasks.train import train_model_task
import redis
import json
import os

router = APIRouter()

# Redis connect
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)
    
# Training task create
@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session=Depends(get_db), email: str=Depends(get_current_user)):
    # find user using email
    from app.models.user import User # 순환 참조 방지용
    user = db.query(User).filter(User.email == email).first()

    db_job = Job(
        user_id=user.id,
        epochs=job.epochs,
        batch_size=job.batch_size,
        status="pending",
        progress=0.0
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # celery task 실행
    train_model_task.delay(db_job.id, job.epochs, job.batch_size)

    return db_job

# Training task list look up
@router.get("/jobs", response_model=list[JobResponse])
def get_jobs(email: str=Depends(get_current_user), db: Session=Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

# Training task detail look up
@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, email: str=Depends(get_current_user), db: Session=Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    return job

# WebSocket endpoint
@router.websocket("/ws/jobs/{job_id}")
async def job_progress_websocket(websocket: WebSocket, job_id: int):
    await websocket.accept()

    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"job_{job_id}_progress")

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)

                if data.get("status") in ["completed", "failed"]:
                    break
    except WebSocketDisconnect:
        pass
    finally:
        pubsub.unsubscribe(f"job_{job_id}_progress")