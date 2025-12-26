from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .models import SessionType
from app.domain.vocab.schemas import TranslationDetail


# SessionConfig Schemas
class SessionConfigBase(BaseModel):
    native_language: str
    language_tested: str
    difficulty: Optional[str] = None
    domain: Optional[str] = None
    session_type: SessionType

class SessionConfigCreate(SessionConfigBase):
    pass

class SessionConfigUpdate(BaseModel):
    native_language: Optional[str] = None
    language_tested: Optional[str] = None
    difficulty: Optional[str] = None
    domain: Optional[str] = None

class SessionConfigSchema(SessionConfigBase):
    id: str
    user_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Session Schemas
class SessionCreate(BaseModel):
    config_id: str
    source_lang_code: str
    target_lang_code: str
    domain: Optional[str] = None
    difficulty: Optional[str] = None
    session_type: SessionType

class SessionUpdate(BaseModel):
    score: Optional[int] = None
    completed_at: Optional[datetime] = None

class SessionSchema(SessionCreate):
    id: str
    user_id: str
    config_id: str
    created_at: datetime
    score: Optional[int] = None
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# SessionResult Schemas
class SessionResultCreate(BaseModel):
    translation_id: int
    correct: bool

class SessionResultSchema(SessionResultCreate):
    id: str
    session_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SessionResultDetail(SessionResultSchema):
    """Extended result with translation details"""
    translation: TranslationDetail
    model_config = ConfigDict(from_attributes=True)


# Session with Results
class SessionDetail(SessionSchema):
    results: List[SessionResultDetail] = []
    model_config = ConfigDict(from_attributes=True)


# UserProgress Schemas
class UserProgressBase(BaseModel):
    translation_id: str

class UserProgressCreate(UserProgressBase):
    pass

class UserProgressUpdate(BaseModel):
    correct_count: Optional[int] = None
    incorrect_count: Optional[int] = None
    last_reviewed: Optional[datetime] = None

class UserProgressSchema(UserProgressBase):
    id: str
    user_id: str
    correct_count: int
    incorrect_count: int
    last_reviewed: datetime
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserProgressDetail(UserProgressSchema):
    """Extended progress with translation details"""
    translation: TranslationDetail
    model_config = ConfigDict(from_attributes=True)
