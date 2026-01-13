import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Jobs from "./pages/Jobs"
import Predict from "./pages/Predict"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/predict" element={<Predict />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;