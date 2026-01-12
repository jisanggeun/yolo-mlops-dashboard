# Backend 

## 📁 Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI APP 진입 포인트
│   ├── config.py        # 환경 설정
│   ├── database.py      # DB 연결
│   ├── api/
│   │   └── auth.py      # 인증 API
│   ├── models/
│   │   └── user.py      # User 테이블
│   ├── schemas/
│   │   └── user.py      # Request/Response Schema
│   └── services/
│       └── auth.py      # 비밀번호 Hashing
├── requirements.txt
└── .env
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

자세한 API 문서: http://localhost:8000/docs