import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { getTokenInfo, refreshToken } from "../api/auth";

function Navbar() {
    const navigate = useNavigate();
    const location = useLocation(); // 현재 path
    const [tokenInfo, setTokenInfo] = useState(null);
    const [remainingTime, setRemainingTime] = useState({ minutes: 0, seconds: 0 });
    const token = localStorage.getItem("token");
    const isChecking = useRef(false);
    const [isRefreshing, setIsRefreshing] = useState(false);

    useEffect(() => {
        if(token) {
            checkToken();
            // 1분마다 token check
            const interval = setInterval(checkToken, 60000);
            return () => clearInterval(interval); // 메모리 누수 방지
        } else {
            setTokenInfo(null); // token 없으면 info 초기화
        }
    }, [token]); // token 값 바뀔 때마다 실행

    // 눈 속임용 frontend 단에서 count down
    useEffect(() => {
        if(tokenInfo) {
            setRemainingTime({
                minutes: tokenInfo.remaining_minutes,
                seconds: tokenInfo.remaining_seconds
            });

            const countdown = setInterval(() => {
                setRemainingTime(prev => {
                    if(prev.seconds > 0) {
                        return { ...prev, seconds: prev.seconds - 1 };
                    } else if(prev.minutes > 0) {
                        return { minutes: prev.minutes - 1, seconds: 59 };
                    } else {
                        return { minutes: 0, seconds: 0 };
                    }
                });
            }, 1000);

            return () => clearInterval(countdown);
        }
    }, [tokenInfo]);

    const checkToken = async () => {
        if(isChecking.current) return;
        isChecking.current = true;

        const info = await getTokenInfo();
        if(info && info.remaining_minutes >= 0) {
            setTokenInfo(info);
        } else {
            // token 만료
            localStorage.removeItem("token");
            setTokenInfo(null);
            navigate("/login");
        }

        isChecking.current = false;
    };

    // 로그아웃
    const handleLogout = () => {
        localStorage.removeItem("token");
        setTokenInfo(null);
        navigate("/login");
    };

    // 새로고침
    const handleRefresh = async () => {
        if(isChecking.current) return;
        isChecking.current = true;
        setIsRefreshing(true);

        const result = await refreshToken();
        if(result) {
            const newInfo = await getTokenInfo();
            setTokenInfo(newInfo);
        }

        // 10초 쿨타임
        setTimeout(() => {
            isChecking.current = false;
            setIsRefreshing(false);
        }, 10000);
    };

    return (
        <nav>
            <Link to="/" className="logo">🔵 YOLO MLOps</Link>
            <div>
                {token ? (
                    <>
                        <Link to="/jobs" className={location.pathname === "/jobs" ? "active" : ""}>학습</Link>
                        <Link to="/predict" className={location.pathname === "/predict" ? "active" : ""}>예측</Link>
                        <Link to="/monitor" className={location.pathname === "/monitor" ? "active" : ""}>모니터링</Link>
                        {tokenInfo && (
                            <span style={{ color: "#aaa", fontSize: "12px", marginRight: "10px" }}>
                                {remainingTime.minutes}분 {remainingTime.seconds}초 남음
                                <button
                                    onClick={handleRefresh}
                                    disabled={isRefreshing}
                                    style={{
                                        marginLeft: "5px",
                                        padding: "2px 8px",
                                        fontSize: "10px",
                                        backgroundColor: isRefreshing ? "#aaa" : "#4fc3f7",
                                        border: "none",
                                        borderRadius: "3px",
                                        color: "white",
                                        cursor: "pointer"
                                    }}
                                >{isRefreshing ? "대기" : "갱신"}</button>
                            </span>
                        )}
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