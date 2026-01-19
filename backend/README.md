# Backend 

## 📁 Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI APP 진입 포인트
│   ├── config.py        # 환경 설정
│   ├── database.py      # DB 연결
│   ├── celery_app.py    # Celery 설정
│   ├── api/
│   │   ├── auth.py        # 인증 API
│   │   ├── jobs.py        # 학습 API + WebSocket
│   │   ├── predict.py     # 예측 API
│   │   └── monitor.py     # 모니터링 API
│   ├── models/
│   │   ├── user.py      # User 테이블
│   │   └── job.py       # Job 테이블
│   ├── schemas/
│   │   ├── user.py      # User 스키마
│   │   ├── job.py       # Job 스키마
│   │   └── predict.py   # Predict 스키마
│   └── services/
│   │   └── auth.py      # 비밀번호 Hashing, JWT
│   └── tasks/
│       └── train.py     # Celery 학습 작업
├── scripts/
│   └── convert_exdark.py # YOLO 형식 변환 
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Run
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧪 Test
```bash
pip install pytest pytest-asyncio
pytest tests/ -v
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | 회원가입 |
| POST | /api/login | 로그인 |
| GET | /api/token/verify | 토큰 유효성 확인 |
| GET | /api/token/info | 토큰 정보 (남은 시간) |
| POST | /api/token/refresh | 토큰 갱신 |
| POST | /api/jobs | 학습 작업 생성 |
| GET | /api/jobs | 학습 작업 목록 조회 |
| GET | /api/jobs/{job_id} | 학습 작업 상세 조회 |
| WS | /api/ws/jobs/{job_id} | 실시간 진행률 WebSocket |
| POST | /api/predict | 이미지 예측 (YOLO) |
| GET | /api/predict/models | 모델 목록 조회 |
| GET | /api/predict/history | 예측 히스토리 조회 |
| GET | /api/predict/image/{timestamp}/{filename} |  예측 이미지 조회 |
| GET | /api/monitor | 시스템 모니터링 (CPU, Memory, GPU) |

자세한 API 문서: http://localhost:8000/docs

## 📦 Dataset
ExDark 데이터셋 사용 (야간 객체 탐지)
- 다운로드: https://github.com/cs-chan/Exclusively-Dark-Image-Dataset
- 변환: `python scripts/convert_exdark.py`