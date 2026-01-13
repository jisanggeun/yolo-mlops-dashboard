import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";

function Login() {
    // 입력 값 저장 (React 메모리)
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    
    const navigate = useNavigate();

    // form 제출 시 실행
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // 검증
        if (!email || !password) {
            setMessage("모든 필드를 입력해주세요.");
            return;
        }

        try {
            const data = await login(email, password);

            // JWT token 저장 
            localStorage.setItem("token", data.access_token);
            navigate("/"); // 로그인 성공 시 home page로 이동
        } catch (error) {
            const detail = error.response?.data?.detail;
            if(typeof detail === "string") {
                setMessage(detail);
            } else if(Array.isArray(detail)) {
                setMessage(detail[0].msg || "로그인 실패");
            } else {
                setMessage("로그인 실패");
            }
        }
    };

    return (
        <div className="auth-card">
            <h1>로그인</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="email"
                    placeholder="이메일"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input 
                    type="password"
                    placeholder="비밀번호"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">로그인</button>
            </form>
            {message && <p className="message">{message}</p>}
        </div>
    );
}

export default Login;