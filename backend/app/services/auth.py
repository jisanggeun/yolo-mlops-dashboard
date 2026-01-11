from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해싱 (회원가입 시 사용)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token 생성 
def create_access_token(data: dict) -> str:
	to_encode = data.copy() # 원본 데이터(이메일) 복사
	# 로그인 만료 시간 계산(현재 시간 + 30분) 
	expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire}) # 로그인 만료 시간을 원본 데이터에 추가
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # HS256 방식으로 해싱