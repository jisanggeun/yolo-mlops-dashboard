from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    check_password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True