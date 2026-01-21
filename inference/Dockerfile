FROM nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir numpy==1.23.5

RUN pip3 install --no-cache-dir fastapi uvicorn python-multipart

RUN pip3 install --no-cache-dir onnx onnxslim

RUN pip3 install --no-cache-dir ultralytics --no-deps
RUN pip3 install --no-cache-dir py-cpuinfo tqdm pyyaml matplotlib pillow requests scipy seaborn pandas psutil

RUN pip3 uninstall -y opencv-python opencv-python-headless 2>/dev/null || true

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]