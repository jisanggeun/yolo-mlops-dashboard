import { useState, useEffect, useRef } from "react";
import { createJob, getJobs } from "../api/jobs";

function Jobs() {
    // 입력 값 저장
    const [epochs, setEpochs] = useState('');
    const [batchSize, setBatchSize] = useState('');
    const [message, setMessage] = useState("");
    const [jobs, setJobs] = useState([]);
    const wsRef = useRef(null);

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

    // WebSocket connect
    const connectWebSocket = (jobId) => {
        const ws = new WebSocket(`ws://localhost:8000/api/ws/jobs/${jobId}`);
        wsRef.current = ws;

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);

            // 해당 job 진행률 update
            setJobs(prevJobs =>
                prevJobs.map(job =>
                    job.id === data.job_id
                        ? {...job, progress: data.progress, status: data.status }
                        : job
                )
            );
            
            // completed / failed 시 종료
            if(data.status === "completed" || data.status === "failed") {
                ws.close();
            }
        };
        
        // error 발생 
        ws.onerror = () => {
            setMessage("WebSocket 연결 실패");
        };
    };

    // Training task create 
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 검증
        if(!epochs || !batchSize || epochs <= 0 || batchSize <= 0) {
            setMessage("Epochs와 Batch Size는 1 이상이어야 합니다.");
            return;
        }

        try {
            const newJob = await createJob(epochs, batchSize);
            setMessage("학습 작업 생성 성공");
            await fetchJobs(); // list 새로 고침
            
            // WebSocket connect
            connectWebSocket(newJob.id);
        } catch (error) {
            setMessage(error.response?.data?.detail || "학습 작업 생성 실패");
        }
    };

    // Component unmount 시 WebSocket 정리
    useEffect(() => {
        return () => {
            if(wsRef.current) {
                wsRef.current.close();
            }
        }
    }, []);

    return (
        <div className="main">
            <div className="card">
                <h2 className="card-title">학습 작업 생성</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Epochs:</label>
                        <input 
                            type="number"
                            min="1"
                            value={epochs}
                            onChange={(e) => setEpochs(e.target.value === "" ? "" : Number(e.target.value))}
                        />
                        <label>Batch Size:</label>
                        <input
                            type="number"
                            min="1"
                            value={batchSize}
                            onChange={(e) => setBatchSize(e.target.value === "" ? "" : Number(e.target.value))}
                        />
                        <button type="submit">학습 시작</button>
                    </div>
                </form>
                {message && <p className="message">{message}</p>}
            </div>
            <div className="card">
                <h2 className="card-title">작업 목록</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>상태</th>
                            <th>진행도</th>
                            <th>Epochs</th>
                            <th>Batch Size</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.map((job) => (
                            <tr key={job.id}>
                                <td>{job.id}</td>
                                <td>
                                    <span className={
                                        job.status === "completed" ? "status-completed" :
                                        job.status === "running" ? "status-running" :
                                        job.status === "failed" ? "status-failed" : 
                                        "status-pending"
                                    }>
                                        {job.status}
                                    </span>
                                </td>
                                <td>
                                    <div style={{
                                        width: "100px",
                                        backgroundColor: "#ddd",
                                        borderRadius: "5px",
                                        overflow: "hidden"
                                    }}>
                                        <div style={{
                                            width: `${job.progress}%`,
                                            backgroundColor: "#4fc3f7",
                                            height: "20px",
                                            borderRadius: "5px",
                                            transition: "width 0.3s"
                                        }}></div>
                                    </div>
                                    <span style={{ marginLeft: "10px" }}>{job.progress.toFixed(1)}%</span>
                                </td>
                                <td>{job.epochs}</td>
                                <td>{job.batch_size}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default Jobs;
