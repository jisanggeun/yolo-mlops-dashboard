import { Link, useNavigate, useLocation } from "react-router-dom";

function Navbar() {
    const navigate = useNavigate();
    const location = useLocation(); // 현재 path
    const token = localStorage.getItem("token");

    // 로그아웃
    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <nav>
            <Link to="/" className="logo">🔵 YOLO MLOps</Link>
            <div>
                {token ? (
                    <>
                        <Link to="/jobs" className={location.pathname === "/jobs" ? "active" : ""}>학습</Link>
                        <Link to="/predict" className={location.pathname === "/predict" ? "active" : ""}>예측</Link>
                        <button onClick={handleLogout}>로그아웃</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className={location.pathname === "/login" ? "active" : ""}>로그인</Link>
                        <Link to="/register" className={location.pathname === "/register" ? "active" : ""}>회원가입</Link>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;