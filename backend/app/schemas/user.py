from pydantic import BaseModel, EmailStr

# 회원가입 request
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    check_password: str

# 회원가입 response
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# 로그인 request
class UserLogin(BaseModel):
	email: EmailStr 
	password: str

# 로그인 response
class Token(BaseModel):
	access_token: str # JWT Token 값
	token_type: str = "bearer" # Token type