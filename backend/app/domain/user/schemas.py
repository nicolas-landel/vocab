from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None
    native_language: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    native_language: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    native_language: Optional[str] = None
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

class UserLanguageBase(BaseModel):
    language_code: str
    level: str  # 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'NATIVE'
    is_learning: bool = True

class UserLanguageCreate(UserLanguageBase):
    pass

class UserLanguageUpdate(BaseModel):
    level: Optional[str] = None
    is_learning: Optional[bool] = None

class UserLanguageResponse(UserLanguageBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserProfileUpdate(BaseModel):
    native_language: Optional[str] = None
    full_name: Optional[str] = None

class UserProfileResponse(UserResponse):
    languages: List[UserLanguageResponse] = []
