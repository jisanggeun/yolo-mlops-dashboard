from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.services.auth import get_current_user
from ultralytics import YOLO
import threading

router = APIRouter()

# Training function (백그라운드 실행)
def train_model(job_id: int, epochs: int, batch_size: int, db_url: str):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(db_url)
    session_local = sessionmaker(bind=engine)
    db = session_local()

    try:
        # update status (running)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "running"
        job.progress = 0.0
        db.commit()

        model = YOLO("yolov8n.pt")

        def on_train_epoch_end(trainer):
            current_epoch = trainer.epoch + 1
            total_epochs = trainer.epochs
            progress = (current_epoch / total_epochs) * 100
	        
            job = db.query(Job).filter(Job.id == job_id).first()
            job.progress = progress
            db.commit()

        model.add_callback("on_train_epoch_end", on_train_epoch_end)

        model.train(
            data="datasets/exdark/yolo/exdark.yaml",
            epochs=epochs,
            batch=batch_size,
            project="runs/train",
            name=f"job_{job_id}",
            exist_ok=True
        )

        # update status (completed)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "completed"
        job.progress = 100.0
        db.commit()

    except Exception as e:
        # update status (failed)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "failed"
        db.commit()
        print(f"학습 실패: {e}")

    finally:
        db.close() 
    
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

    # 백그라운드 학습 시작
    from app.config import settings
    thread = threading.Thread(
        target=train_model,
        args=(db_job.id, job.epochs, job.batch_size, settings.DATABASE_URL)
    )
    thread.start()

    return db_job

# Training task list look up
@router.get("/jobs", response_model=list[JobResponse])
def get_jobs(db: Session=Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

# Training task detail look up
@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session=Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
    return job
