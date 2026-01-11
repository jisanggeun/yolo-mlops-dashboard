from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str="mysql+pymysql://user:password@localhost:3306/yolo_mlops"

    class Config:
        env_file = ".env"

settings = Settings()
