# Backend 

## 📁 Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI APP 진입 포인트
│   ├── config.py        # 환경 설정
│   ├── database.py      # DB 연결
│   ├── api/
│   │   ├── auth.py      # 인증 API
│   │   ├── jobs.py      # 학습 작업 API
│   │   └── predict.py   # 예측 API
│   ├── models/
│   │   ├── user.py      # User 테이블
│   │   └── job.py       # Job 테이블
│   ├── schemas/
│   │   ├── user.py      # User 스키마
│   │   ├── job.py       # Job 스키마
│   │   └── predict.py   # Predict 스키마
│   └── services/
│       └── auth.py      # 비밀번호 Hashing, JWT
├── requirements.txt
├── .env
└── README.md
```

## 🚀 실행
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | 회원가입 |
| POST | /api/login | 로그인 |
| POST | /api/jobs | 학습 작업 생성 |
| GET | /api/jobs | 학습 작업 목록 조회 |
| GET | /api/jobs/{job_id} | 학습 작업 상세 조회 |
| POST | /api/predict | 이미지 예측 (YOLO) |
| GET | /api/predict/history | 예측 히스토리 조회 |
| GET | /api/predict/image/{timestamp}/{filename} |  예측 이미지 조회 |

자세한 API 문서: http://localhost:8000/docs