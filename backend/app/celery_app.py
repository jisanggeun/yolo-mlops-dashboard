from celery import Celery
import os

# Redis URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# create celery app
celery_app = Celery(
    "yolo_mlops",
    broker=REDIS_URL, # task queue (Redis)
    backend=REDIS_URL, # result 저장소 (Redis)
    include=["app.tasks.train"]
)

# setting
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True
)