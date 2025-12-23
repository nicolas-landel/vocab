from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    native_language: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    native_language: Optional[str] = None
    learning_languages: Optional[List[str]] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    native_language: Optional[str] = None
    learning_languages: Optional[List[str]] = []
    oauth_provider: Optional[str] = None
    full_name: Optional[str] = None
    picture_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class GoogleAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

