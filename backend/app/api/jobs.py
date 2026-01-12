from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

# Training task create
@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session=Depends(get_db), email: str=Depends(get_current_user)):
    # find user using email
    user = db.query(User).filter(User.email == email).first()

    new_job = Job(
        user_id=user.id,
        epochs=job.epochs,
        batch_size=job.batch_size
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

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
