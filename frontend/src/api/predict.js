import axios from "axios";

const API_URL = "http://localhost:8000/api";

// 모델 목록 조회
export const getModels = async () => {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_URL}/predict/models`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
}

// Image Predict API 호출
export const predict = async (file, modelName="pretrained") => {
    const token = localStorage.getItem("token");
    // 파일 전송을 위한 FormData
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
        `${API_URL}/predict?model_name=${modelName}`, 
        formData, {
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-type": "multipart/form-data"
        }
    });
    return response.data;
};

// 과거 예측 목록 조회
export const getPredictHistory = async () => {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_URL}/predict/history`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
};