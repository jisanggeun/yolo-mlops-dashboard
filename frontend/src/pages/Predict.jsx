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
        <div>
            <h1>이미지 예측</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="file"
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files[0])}
                /> {/* --> 첫 번째 파일 저장 */}
                <button type="submit">예측하기</button>
            </form>
            {message && <p>{message}</p>}

            {result && (
                <div>
                    <h2>결과</h2>
                    <p>파일명: {result.filename}</p>
                    <ul>
                        {result.predictions.map((pred, index) => (
                            <li key={index}>
                                {pred.class} - {(pred.confidence * 100).toFixed(1)}% 
                                {/* 예측 클래스 - conf_score * 100 %(소수점 둘째 자리에서 반올림) */}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default Predict;