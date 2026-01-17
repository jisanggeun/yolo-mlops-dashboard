# Python image
FROM python:3.9-slim

# work directory
WORKDIR /app

# system package
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# dependency 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# code 
COPY . .

# port 
EXPOSE 8000

# server 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]