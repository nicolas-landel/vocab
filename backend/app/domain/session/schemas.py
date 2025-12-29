from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .models import SessionType
from app.domain.vocab.schemas import TranslationDetail
from uuid import UUID


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
    id: UUID
    user_id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Session Schemas
class SessionCreate(BaseModel):
    config_id: UUID
    source_lang_code: str
    target_lang_code: str
    domain: Optional[str] = None
    difficulty: Optional[str] = None
    session_type: SessionType

class SessionUpdate(BaseModel):
    score: Optional[int] = None
    completed_at: Optional[datetime] = None

class SessionSchema(SessionCreate):
    id: UUID
    user_id: UUID
    config_id: UUID
    created_at: datetime
    score: Optional[int] = None
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# SessionWord Schemas
class SessionWordCreate(BaseModel):
    translation_from_id: UUID
    translation_to_id: UUID
    from_language: str
    to_language: str
    correct: Optional[bool] = None
    user_answer: Optional[str] = None

class SessionWordSchema(SessionWordCreate):
    id: UUID
    session_id: UUID
    translation_from_id: UUID
    translation_to_id: UUID
    from_language: str
    to_language: str
    correct: Optional[bool] = None
    user_answer: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SessionWordDetail(SessionWordSchema):
    """Extended result with translation details"""
    translation_from: TranslationDetail
    translation_to: TranslationDetail
    model_config = ConfigDict(from_attributes=True)


# Session with Results
class SessionDetail(SessionSchema):
    results: List[SessionWordDetail] = []
    model_config = ConfigDict(from_attributes=True)


# UserProgress Schemas
class UserProgressBase(BaseModel):
    translation_id: UUID

class UserProgressCreate(UserProgressBase):
    pass

class UserProgressUpdate(BaseModel):
    correct_count: Optional[int] = None
    incorrect_count: Optional[int] = None
    last_reviewed: Optional[datetime] = None

class UserProgressSchema(UserProgressBase):
    id: UUID
    user_id: UUID
    correct_count: int
    incorrect_count: int
    last_reviewed: datetime
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserProgressDetail(UserProgressSchema):
    """Extended progress with translation details"""
    translation: TranslationDetail
    model_config = ConfigDict(from_attributes=True)
