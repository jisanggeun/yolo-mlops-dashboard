# Frontend

## 📁 Structure
```
frontend/
├── src/
│   ├── api/
│   │   ├── auth.js        # Auth API (로그인, 토큰 관리)
│   │   ├── jobs.js        # Jobs API
│   │   ├── predict.js     # Predict API
│   │   └── monitor.js     # Monitor API
│   ├── components/
│   │   └── Navbar.jsx     # Navigation Bar (토큰 카운트다운)
│   ├── pages/
│   │   ├── Register.jsx   # Register 페이지
│   │   ├── Login.jsx      # Login 페이지
│   │   ├── Jobs.jsx       # Jobs 페이지 (실시간 진행도)
│   │   ├── Predict.jsx    # Predict Page (모델 선택, 히스토리)
│   │   └── Monitor.jsx    # Monitor Page (시스템 모니터링)
│   ├── App.js
│   └── index.js
│   └── index.css          # Global Styles
├── public/
└── package.json
```

## 🚀 실행
```bash
npm install
npm start
```

## 📡 Pages
| Page | Path | Description |
|------|------|-------------|
| Home | / | 대시보드 홈 |
| Register | /register | 회원가입 |
| Login | /login | 로그인 |
| Jobs | /jobs | 학습 작업 관리 (WebSocket 실시간 진행도) |
| Predict | /predict | 이미지 예측 (모델 선택, 히스토리) |
| Monitor | /monitor | 시스템 모니터링 (CPU, Memory, GPU) |

## 🔐 Token
| Feature | Description |
|------|------|
| 남은 시간 표시 | 분/초 카운트다운 |
| 자동 갱신 | 1분마다 토큰 확인 |
| 수동 갱신 | 갱신 버튼 (10초 쿨타임) |