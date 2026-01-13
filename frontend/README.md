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
│   │   ├── Register.jsx   # Register Page
│   │   ├── Login.jsx      # Login Page
│   │   ├── Jobs.jsx       # Jobs Page
│   │   └── Predict.jsx    # Predict Page
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
| Home | / | Dashboard Home |
| Register | /register | Register Form |
| Login | /login | Login Form |
| Jobs | /jobs | Training Job Management |
| Predict | /predict | Image Upload + Result |