from fastapi import APIRouter, Depends
from app.services.auth import get_current_user
import psutil
import GPUtil

router = APIRouter()

@router.get("/monitor")
def get_system_status(email: str=Depends(get_current_user)):
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # Memory
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_used = memory.used / (1024 ** 3) # GB
    memory_total = memory.total / (1024 ** 3) # GB

    # GPU
    gpu_info = []
    try: 
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_info.append({
                "name": gpu.name,
                "load": gpu.load * 100, # %
                "memory_used": gpu.memoryUsed, # MB
                "memory_total": gpu.memoryTotal, # MB
                "memory_percent": (gpu.memoryUsed / gpu.memoryTotal) * 100,
                "temperature": gpu.temperature
            })
    except:
        gpu_info = []

    return {
        "cpu": {
            "percent": cpu_percent
        }, "memory": {
            "percent": memory_percent,
            "used_gb": round(memory_used, 2),
            "total_gb": round(memory_total, 2)
        }, "gpu": gpu_info
    }