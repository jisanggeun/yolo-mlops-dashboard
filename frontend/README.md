# Frontend

## 📁 Structure
```
frontend/
├── src/
│   ├── api/
│   │   ├── auth.js        # Auth API
│   │   ├── jobs.js        # Jobs API
│   │   └── predict.js     # Predict API
│   ├── components/
│   │   └── Navbar.jsx     # Navigation Bar
│   ├── pages/
│   │   ├── Register.jsx   # Register 페이지
│   │   ├── Login.jsx      # Login 페이지
│   │   ├── Jobs.jsx       # Jobs 페이지 (실시간 진행도)
│   │   └── Predict.jsx    # Predict 페이지 (모델 선택, 히스토리)
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
| Jobs | /jobs | 학습 작업 관리 (실시간 진행도) |
| Predict | /predict | 이미지 예측 (모델 선택, 히스토리) |