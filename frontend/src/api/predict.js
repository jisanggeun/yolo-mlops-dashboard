import axios from "axios";

const API_URL = "http://localhost:8000/api";

// Image Predict API 호출
export const predict = async (file) => {
    const token = localStorage.getItem("token");
    // 파일 전송을 위한 FormData
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-type": "multipart/form-data"
        }
    });
    return response.data;
}