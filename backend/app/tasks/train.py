from app.celery_app import celery_app
from app.database import session_local
from ultralytics import YOLO
from app.models.user import User
from app.models.job import Job
import os
import yaml
import redis
import json
import mlflow
import mlflow.pytorch

# Redis connect
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, db=0, decode_responses=True)

# MLflow setting
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))

# 학습 저장 경로 (backend/runs/train)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TRAIN_DIR = os.path.join(BASE_DIR, "runs", "train")

def create_dataset_yaml():
    dataset_path = os.getenv("DATASET_PATH", os.path.join(BASE_DIR, "datasets", "exdark", "yolo"))

    yaml_content = {
        "path": dataset_path,
        "train": "images/train",
        "val": "images/val",
        "names": {
            0: "Bicycle",
            1: "Boat",
            2: "Bottle",
            3: "Bus",
            4: "Car",
            5: "Cat",
            6: "Chair",
            7: "Cup",
            8: "Dog",
            9: "Motorbike",
            10: "People",
            11: "Table"
        }
    }

    yaml_path = os.path.join(dataset_path, "exdark.yaml")
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

    return yaml_path

def publish_progress(job_id: int, progress: float, status: str, epoch: int=0, total: int=0):
    # Redis Pub/Sub으로 진행률 전송
    data = {
        "job_id": job_id,
        "progress": progress,
        "status": status,
        "epoch": epoch,
        "total": total
    }
    redis_client.publish(f"job_{job_id}_progress", json.dumps(data))

@celery_app.task(bind=True)
def train_model_task(self, job_id: int, epochs: int, batch_size: int):
    db = session_local()

    try:
        # update status (running)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "running"
        job.progress = 0.0
        db.commit()
        
        # 진행률 전송
        publish_progress(job_id, 0.0, "running", 0, epochs)

        # yaml file dynamic create
        yaml_path = create_dataset_yaml()

        # YOLO model load
        model = YOLO("yolov8n.pt")

        # epoch 끝날 때마다 progres update
        def on_train_epoch_end(trainer):
            current_epoch = trainer.epoch + 1
            total_epochs = trainer.epochs
            progress = (current_epoch / total_epochs) * 100

            job = db.query(Job).filter(Job.id == job_id).first()
            job.progress = progress
            db.commit()

            # Redis Pub/Sub 전송
            publish_progress(job_id, progress, "running", current_epoch, total_epochs)

            # update celery status
            self.update_state(
                state="PROGRESS",
                meta={"progress": progress, "epoch": current_epoch, "total": total_epochs}
            )

        # call back
        model.add_callback("on_train_epoch_end", on_train_epoch_end)

        # train start 전에 폴더 생성
        os.makedirs(os.path.join(TRAIN_DIR, f"job_{job_id}"), exist_ok=True)

        # train start
        model.train(
            data=yaml_path,
            epochs=epochs,
            batch=batch_size,
            project=TRAIN_DIR,
            name=f"job_{job_id}",
            exist_ok=True,
            workers=0
        )

        # MLflow
        results_dir = os.path.join(TRAIN_DIR, f"job_{job_id}")

        with mlflow.start_run(run_name=f"job_{job_id}"):
            # save parameter
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("batch_size", batch_size)
            mlflow.log_param("model", "yolov8n")
            mlflow.log_param("dataset", "exdark")
            
            # save best.pt
            model_path = os.path.join(results_dir, "weights", "best.pt")
            if os.path.exists(model_path):
                mlflow.log_artifact(model_path, "model")

            # save last.pt
            last_model_path = os.path.join(results_dir, "weights", "last.pt")
            if os.path.exists(last_model_path):
                mlflow.log_artifact(last_model_path, "model")


        # update status (completed)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "completed"
        job.progress = 100.0
        db.commit()

        publish_progress(job_id, 100.0, "completed", epochs, epochs)

        return {
            "status": "completed",
            "job_id": job_id
        }
    
    except Exception as e:
        # update status (failed)
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "failed"
        db.commit()

        publish_progress(job_id, 0.0, "failed", 0, 0)

        return {
            "status": "failed",
            "job_id": job_id,
            "error": str(e)
        }
    
    finally:
        db.close()