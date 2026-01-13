import axios from "axios";

const API_URL = "http://localhost:8000/api"

// Training task create
export const createJob = async (epochs, batchSize) => {
    const token = localStorage.getItem("token");
    const response = await axios.post(`${API_URL}/jobs`, {
        epochs,
        batch_size: batchSize
    }, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};

// Training task list look up
export const getJobs = async () => {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_URL}/jobs`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};

// Training task detail look up
// 나중에 상세 페이지 만들 때 사용 예정
export const getJob = async (jobId) => {
    const token = localStorage.getItem("token");
    const response = await axios.get(`${API_URL}/jobs/${jobId}`, {
        headers:{
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
}