import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Jobs from "./pages/Jobs"
import Predict from "./pages/Predict"

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={
          <div className="main">
            <h1 className="home-title">🚀 YOLO MLOps Dashboard</h1>
            <p className="home-subtitle">AI 기반 객체 탐지 모델 학습 & 예측 플랫폼</p>
          </div>
        } />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/predict" element={<Predict />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;