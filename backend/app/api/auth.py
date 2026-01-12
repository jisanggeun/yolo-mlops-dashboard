from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter()

# 회원가입
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session=Depends(get_db)):
    if user.password != user.check_password:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# 로그인
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    # 해당하는 유저 찾기
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user: 
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
    
    # 비밀번호 검증
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
    
    # Token 생성 / JWT 표준 규칙 (sub: 토큰 주인, exp: 만료 시간, iat: 발급 시간)
    access_token = create_access_token({"sub": db_user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}