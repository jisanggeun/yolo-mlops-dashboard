import axios from "axios";

const API_URL = "http://localhost:8000/api";

// 회원가입 API 호출
export const register = async(email, password, checkPassword) => {
    // 백엔드 /api/register로 POST 요청
    const response = await axios.post(`${API_URL}/register`, {
        email,
        password,
        check_password: checkPassword
    });
    
    // 백엔드 response data return (id, email)
    return response.data;
};