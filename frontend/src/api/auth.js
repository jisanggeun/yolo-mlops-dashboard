import axios from "axios";

const API_URL = "http://localhost:8000/api";

// 회원가입 API 호출
export const register = async (email, password, checkPassword) => {
    // 백엔드 /api/register로 POST 요청
    const response = await axios.post(`${API_URL}/register`, {
        email,
        password,
        check_password: checkPassword
    });
    
    // 백엔드 response data return (id, email)
    return response.data;
};

// 로그인 API 호출
export const login = async (email, password) => {
    // 백엔드 /api/login으로 POST 요청
    const response = await axios.post(`${API_URL}/login`, 
        // login = form 방식
        new URLSearchParams({
            username: email,
            password
        }), {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }
    );
    // login.jsx로 token return
    return response.data
};

// token 유효성 확인
export const verifyToken = async () => {
    const token = localStorage.getItem("token");
    if(!token) return { valid: false };

    try {
        const response = await axios.get(`${API_URL}/token/verify`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch(error) {
        return { valid: false };
    }
};

// token info (만료 시간)
export const getTokenInfo = async () => {
    const token = localStorage.getItem("token");
    if(!token) return null;

    try {
        const response = await axios.get(`${API_URL}/token/info`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    } catch(error) {
        return null;
    }
};

// token 갱신
export const refreshToken = async () => {
    const token = localStorage.getItem("token");
    if(!token) return null;

    try {
        const response = await axios.post(`${API_URL}/token/refresh`, {}, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        localStorage.setItem("token", response.data.access_token);
        return response.data;
    } catch(error) {
        return null;
    }
};