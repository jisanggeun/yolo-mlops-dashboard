import { useState, useEffect } from "react";
import { createJob, getJobs } from "../api/jobs";

function Jobs() {
    // 입력 값 저장
    const [epochs, setEpochs] = useState(100);
    const [batchSize, setBatchSize] = useState(16);
    const [message, setMessage] = useState("");
    const [jobs, setJobs] = useState([]);

    // 페이지 로드 시 task list lookup
    useEffect(() => {
        fetchJobs();
    }, []);

    // Task list look up
    const fetchJobs = async () => {
        try {
            const data = await getJobs();
            setJobs(data);
        } catch (error) {
            setMessage('작업 목록 조회 실패');
        }
    };

    // Training task create 
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 검증
        if(epochs <= 0 || batchSize <= 0) {
            setMessage("Epochs와 Batch Size는 1 이상이어야 합니다.");
            return;
        }

        try {
            await createJob(epochs, batchSize);
            setMessage("학습 작업 생성 성공");
            fetchJobs(); // list 새로 고침
        } catch (error) {
            setMessage(error.response?.data?.detail || "학습 작업 생성 실패");
        }
    };

    return (
        <div>
            <h1>학습 작업</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="number"
                    placeholder="Epochs"
                    value={epochs}
                    onChange={(e) => setEpochs(Number(e.target.value))}
                />
                <input 
                    type="number"
                    placeholder="Batch Size"
                    value={batchSize}
                    onChange={(e) => setBatchSize(Number(e.target.value))}
                />
                <button type="submit">학습 시작</button>
            </form>
            {message && <p>{message}</p>}

            <h2>작업 목록</h2>
            <ul>
                {jobs.map((job) => (
                    <li key={job.id}>
                        ID: {job.id} | 상태: {job.status} | Epochs: {job.epochs} | Batch: {job.batch_size}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Jobs;