# Inference Server

## 📌 Overview
YOLO 모델을 TensorRT로 최적화하여 추론하는 서버 
(Jetson Orin Nano용)

## 📁 Structure
```
inference/
├── main.py         # FastAPI 추론 서버
├── requirements.txt  # 참고용 Dependency list
├── Dockerfile      # Jetson용 Dockerfile
└── README.md
```

## 🚀 Run (Jetson)
```bash
docker build -t yolo-inference .
docker run -d --runtime nvidia -p 8001:8001 yolo-inference
```

## 🔧 TensorRT 자동 변환
- 첫 실행 시 자동으로 `.pt` → `.engine` 변환 (5~10분)
- 이후 실행 시 `.engine` 파일 바로 로드 (몇 초)

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | 서버 상태 확인 |
| POST | /predict | 이미지 추론 (시각화 포함) |
| GET | /models | 현재 모델 정보 |

## 📤 Response Example
```json
{
  "detections": [
    {
      "class": 0,
      "class_name": "person",
      "confidence": 0.85,
      "bbox": [100, 150, 300, 400]
    }
  ],
  "image_base64": "base64 encoded image..."
}
```