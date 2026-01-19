from ultralytics import YOLO

# YOLO model을 TensorRT로 변환 (Jetson에서 실행 예정)
def convert_to_tensorrt(model_path: str, output_path: str=None):
    # .pt model -> tensorRT .engine convert
    model = YOLO(model_path)

    # tensorRT로 export 
    model.export(format="engine", device=0)
    print(f"변환 완료: {model_path} -> TensorRT engine")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: Python convert.py <model_path>")
        print("Example: Python convert.py best.pt")
    else:
        convert_to_tensorrt(sys.argv[1])