import axios from "axios";

const API_URL = "http://localhost:8000/api";

// 시스템 상태 조회 (CPU, Memory, GPU)
export const getSystemStatus = async () => {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_URL}/monitor`, {
        headers: {
            Authorization: `Bearer ${token}` 
        }
    });
    return response.data;
};