import { useState, useEffect } from "react";
import { predict, getPredictHistory } from "../api/predict";

function Predict() {
    // 입력 값 저장
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [result, setResult] = useState(null);
    const [showImage, setShowImage] = useState(false);
    const [history, setHistory] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);

    // page 로드 시 history 조회
    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await getPredictHistory();
            setHistory(data);
        } catch (error) {
            setMessage("히스토리 조회 실패");
        }
    };

    // Form 제출 시 실행되는 함수
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 검증
        if(!file) {
            setMessage("파일을 선택해주세요.");
            return;
        }

        // 이미지 파일 검증
        if(!file.type.startsWith("image/")) {
            setMessage("이미지 파일만 업로드 가능합니다.");
            return;
        }

        try {
            const data = await predict(file);
            setResult(data);
            setMessage("예측 성공");
        } catch (error) {
            setMessage(error.response?.data?.detail || "예측 실패");
        }
    };

    return (
        <div className="main">
            <div className="card">
                <h2 className="card-title">이미지 예측</h2>
                <form onSubmit={handleSubmit}>
                    <div className="file-upload">
                        <p>📁 이미지를 선택하세요.</p>
                        <input 
                            type="file"
                            accept="image/*"
                            onChange={(e) => setFile(e.target.files[0])}
                        />
                    </div>
                    <button type="submit">예측하기</button>
                </form>
                {message && <p className="message">{message}</p>}
            </div>

            {result && (
                <div classsName="card">
                    <h2 className="card-title">예측 결과</h2>
                    <div className="result-card">
                        <p><strong>파일명:</strong> {result.filename}</p>
                        {result.predictions.map((pred, index) => (
                            <div key={index} className="result-item">
                                <span>{pred.class}</span>
                                <span className="confidence">{(pred.confidence * 100).toFixed(1)}%</span>
                            </div>
                        ))}
                    </div>
                    
                    <button 
                        onClick={() => setShowImage(!showImage)}
                        style={{ marginTop:"20px" }}
                    >
                        {showImage ? "시각화 숨기기" : "시각화 보기"}
                    </button>
                    
                    {showImage && (
                        <div style={{ marginTop: "20px" }}>
                            <img
                                src={`http://localhost:8000${result.image_path}`}
                                alt="예측 결과"
                                style={{ maxWidth: "100%", borderRadius: "10px" }}
                            />
                        </div>
                    )}
                </div>
            )}
            
            {history.length > 0 && (
                <div className="card">
                    <h2 className="card-title">예측 히스토리</h2>
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                        {history.map((item, index) => (
                            <div
                                key={index}
                                onClick={() => setSelectedImage(selectedImage === item.image_path ? null : item.image_path)}
                                style={{
                                    cursor: "pointer",
                                    padding: "10px",
                                    border: selectedImage === item.image_path ? "2px solid #4fc3f7" : "1px solid #ddd",
                                    borderRadius: "5px"
                                }}
                            >
                            <p>{item.filename}</p>
                            <p style={{ fontSize: "12px", color: "#666" }}>{item.timestamp}</p>
                            </div>
                        ))}
                    </div>
                    {selectedImage && (
                        <div style={{ marginTop: "20px" }}>
                            <button onClick={() => setSelectedImage(null)}>닫기</button>
                            <img
                                src={`http://localhost:8000${selectedImage}`}
                                alt="과거 예측"
                                style={{ maxWidth: "100%", borderRadius: "10px", marginTop: "10px"}}
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Predict;