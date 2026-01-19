from pydantic_settings import BaseSettings

# 환경 설정 class
class Settings(BaseSettings):
    DATABASE_URL: str="mysql+pymysql://user:password@localhost:3306/yolo_mlops" # DB 연결 주소 (기본 값 설정)
    SECRET_KEY: str="TEST_SECRET_KEY" # JWT 비밀 키
    ALGORITHM: str="HS256" # Hash + SHA256 (JWT)
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30 # Token 만료 시간 30분
    DATASET_PATH: str=""
    REDIS_HOST: str="localhost"
    INFERENCE_SERVER_URL: str="http://localhost:8001"
    MLFLOW_TRACKING_URI: str="http://localhost:5000"

    class Config:
        env_file = ".env" # .env 파일에서 환경변수 가져 옴
        extra = "ignore"

# 설정 객체 생성 (다른 파일에서 import해서 사용하기 때문)
settings = Settings()
