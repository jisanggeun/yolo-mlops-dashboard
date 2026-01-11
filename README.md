# YOLO MLOps Dashboard

## 📌 Overview
    YOLO 기반 객체 탐지 모델 Training과 Predict를 API로 제어하고, 학습 상태와 성능 지표를 웹에서 실시간으로 확인할 수 있는 프로젝트입니다.  
    학습 과정에서의 서버 리소스 사용량을 함께 제공해, 모델 학습과 인프라 상태(CPU, Memory, GPU)를 동시에 파악할 수 있도록 설계했습니다.

---

## 🎯 Project Goals
    - YOLO Model 학습을 API 기반으로 제어
    - 학습 진행 상황 및 성능 지표 시각화
    - WebSocket을 활용한 실시간 학습 상태 전달
    - 인프라 리소스 모니터링 (CPU / Memory / GPU)
    - Docker를 통해 Backend, Frontend, Monitoring 환경을 분리 구성

---

## ✨ System Architecture


---

## 🧩 Tech Stack 
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black) 
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)

![YOLOv8](https://img.shields.io/badge/YOLOv8-00FFFF?style=flat&logo=yolo&logoColor=black)
![TensorRT](https://img.shields.io/badge/TensorRT-76B900?style=flat&logo=nvidia&logoColor=white) 
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=flat&logo=minio&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker_Hub-2496ED?style=flat&logo=docker&logoColor=white)

![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![Loki](https://img.shields.io/badge/Loki-F46800?style=flat&logo=grafana&logoColor=white)