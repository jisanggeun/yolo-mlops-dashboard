import { useState, useEffect } from "react";
import { getSystemStatus } from "../api/monitor";

function Monitor() {
    const [status, setStatus] = useState(null);
    const [message, setMessage] = useState("");

    // 5초마다 status 조회
    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000); 
        return () => clearInterval(interval);
    }, []);

    // system status 조회
    const fetchStatus = async () => {
        try {
            const data = await getSystemStatus();
            setStatus(data);
        } catch(error) {
            setMessage("모니터링 조회 실패");
        }
    };

    // 게이지 바 rendering
    const renderGauge = (percent, color) => (
        <div style={{
            width: "100%",
            height: "20px",
            backgroundColor: "#ddd",
            borderRadius: "10px",
            overflow: "hidden"
        }}>
            <div style={{
                width: `${percent}%`,
                height: "100%",
                backgroundColor: color,
                borderRadius: "10px",
                transition: "width 0.3s"
            }}></div>
        </div>
    );

    // 퍼센티지에 따른 색 변환 
    const getColor = (percent) => {
        if(percent < 50) return "#27ae60";
        if(percent < 80) return "#f39c12";
        return "#e74c3c";
    }

    return (
        <div className="main">
            <div className="card">
                <h2 className="card-title">🖥️ 시스템 모니터링</h2>
                {message && <p className="message">{message}</p>}

                {status && (
                    <div style={{ display: "flex", flexDirection: "column", gap: "30px"}}>
                    {/* CPU */}
                    <div>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px"}}>
                            <span><strong>CPU 사용률</strong></span>
                            <span>{status.cpu.percent}%</span>
                        </div>
                        {renderGauge(status.cpu.percent, getColor(status.cpu.percent))}
                    </div>
                    
                    {/* Memory */}
                    <div>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px"}}>
                            <span><strong>Memory 사용량(사용률)</strong></span>
                            <span>{status.memory.used_gb}GB / {status.memory.total_gb}GB ({status.memory.percent}%)</span>
                        </div>
                        {renderGauge(status.memory.percent, getColor(status.memory.percent))}
                    </div>

                    {/* GPU */}
                    {status.gpu.map((gpu, index) => (
                        <div key={index}>
                            <div style={{ marginBottom: "15px" }}>
                                <strong>GPU: {gpu.name}</strong>
                            </div>

                            <div style={{ marginBottom: "10px" }}>
                                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px"}}>
                                    <span>사용률</span>
                                    <span>{gpu.load.toFixed(1)}%</span>
                                </div>
                                {renderGauge(gpu.load, getColor(gpu.load))}
                            </div>

                            <div style={{ marginBottom: "10px" }}>
                                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px"}}>
                                    <span>메모리 사용량(사용률)</span>
                                    <span>{gpu.memory_used}MB / {gpu.memory_total}MB ({gpu.memory_percent.toFixed(1)}%)</span>
                                </div>
                                {renderGauge(gpu.memory_percent, getColor(gpu.memory_percent))}
                            </div>

                            {/* GPU 온도 */}
                            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px"}}>
                                <span>온도</span>
                                <span>{gpu.temperature}°C</span>
                            </div>
                        </div>
                    ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Monitor;