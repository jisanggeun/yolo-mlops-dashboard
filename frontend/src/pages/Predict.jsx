import { useState } from "react";
import { predict } from "../api/predict";

function Predict() {
    // 입력 값 저장
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [result, setResult] = useState(null);

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
                </div>
            )}
        </div>
    );
}

export default Predict;