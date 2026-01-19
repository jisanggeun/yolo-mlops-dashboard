# Inference Server

## 📌 Overview
YOLO 모델을 TensorRT로 최적화하여 추론하는 서버 
(Jetson Orin Nano용)

## 📁 Structure
```
inference/
├── main.py         # FastAPI 추론 서버
├── convert.py      # YOLO -> TensorRT 변환
├── requirements.txt
├── Dockerfile      # Jetson용 Dockerfile
└── README.md
```

## 🚀 Run (Jetson)
```bash
docker build -t yolo-inference .
docker run -d --runtime nvidia -p 8001:8001 yolo-inference
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | 서버 상태 확인 |
| POST | /predict | 이미지 추론 |
| GET | /models | 현재 모델 정보 |

## 🔧 TensorRT 변환
```bash
python convert.py best.pt
```