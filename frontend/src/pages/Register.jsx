import { useState } from "react";
import { register } from "../api/auth"

function Register() {
    // 입력 값 저장 (React 메모리)
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [checkPassword, setCheckPassword] = useState('');
    const [message, setMessage] = useState('');

    // form 제출 시 실행
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 검증
        if(!email || !password || !checkPassword) {
            setMessage("모든 필드를 입력해주세요.")
            return;
        }

        if(password !== checkPassword) {
            setMessage("비밀번호가 일치하지 않습니다.")
            return;
        }

        // 백엔드 회원가입 API response
        try {
            await register(email, password, checkPassword);
            setMessage("회원가입 성공");
        } catch (error) {
            // error message (옵셔널 체이닝 사용)
            // 값 없으면 error 발생 -> 옵셔널 체이닝 통해 error 대신 undefined 반환
            setMessage(error.response?.data?.detail || "회원가입 실패");
        }
    };

    return (
        <div className="auth-card">
            <h1>회원가입</h1>
            {/* form 제출 시 handleSubmit 실행 */}
            <form onSubmit={handleSubmit}>
                {/* email 입력 */}
                <input 
                    type="email"
                    placeholder="이메일"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                /> 
                {/* 비밀번호 입력 */}
                <input 
                    type="password"
                    placeholder="비밀번호"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /> 
                {/* 비밀번호 확인 입력 */}
                <input 
                    type="password"
                    placeholder="비밀번호 확인"
                    value={checkPassword}
                    onChange={(e) => setCheckPassword(e.target.value)}
                />
                <button type="submit">가입하기</button>
            </form>
            {/* 메세지 있으면 표시 */}
            {message && <p className="message">{message}</p>}
        </div>
    );
} 

export default Register;