from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# request header에서 token 자동 추출
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# 비밀번호 해싱 (회원가입 시 사용)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증 (로그인 시 사용)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token 생성 
def create_access_token(data: dict) -> str:
    to_encode = data.copy() # 원본 데이터(이메일) 복사
	# 로그인 만료 시간 계산(현재 시간 + 30분) 
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # 로그인 만료 시간을 원본 데이터에 추가
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # HS256 방식으로 해싱

# JWT token 복호화 후 이메일 추출
def get_current_user(token: str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
# JWT token info 가져오기 (만료 시간 포함)
def get_token_info(token: str=Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        exp = payload.get("exp")

        if email is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        
        # 남은 시간 계산
        exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        remaining = exp_datetime - datetime.now(timezone.utc)
        remaining_seconds = int(remaining.total_seconds())
        remaining_mins = remaining_seconds // 60
        remaining_secs = remaining_seconds % 60

        return {
            "email": email,
            "expires_at": exp_datetime.isoformat(),
            "remaining_minutes": remaining_mins, # 남은 분
            "remaining_seconds": remaining_secs # 남은 초
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
